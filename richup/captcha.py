"""Cloudflare Turnstile token provider for richup.io.

richup.io requires a `captchaToken` on `join-game`. We mint real tokens by
rendering the site's own Turnstile widget (sitekey 0x4AAAAAAC08XOgqbge2s3TZ)
inside a real Chrome page loaded on https://richup.io — correct hostname,
correct sitekey, no third-party solver.

Two implementation quirks discovered during reverse engineering:

1. The `api.js` script-tag load frequently stalls in this environment (the
   request is sent but the response never completes — likely QUIC/IPv6
   weirdness in Chrome's network stack). Fetching the same bytes with curl
   or `fetch()` works fine. So we fetch api.js out-of-band (urllib) and
   `eval()` the source inside the page — always reliable.

2. `brunhild.challenges.cloudflare.com` (challenge delivery host) is
   IPv6-only in DNS and this machine has no IPv6 route. We pin it to
   Cloudflare's IPv4 edge via --host-resolver-rules so the interactive
   challenge *could* load if ever required. With a clean (non-automated)
   Chrome profile the widget usually passes non-interactively anyway.

Browser choice: `patchright` (stealth playwright) driving real Google
Chrome (`channel="chrome"`), headed — this combination reliably gets a
non-interactive pass. Headless still works sometimes; set
RICHUP_CAPTCHA_HEADLESS=1 to try it.

One token per `get_token()` call; tokens are single-use and ~5 min TTL.
"""

from __future__ import annotations

import asyncio
import logging
import os
import socket
import time
import urllib.request

log = logging.getLogger("richup.captcha")

SITEKEY = "0x4AAAAAAC08XOgqbge2s3TZ"
TURNSTILE_API = "https://challenges.cloudflare.com/turnstile/v0/api.js"
TOKEN_TIMEOUT_S = float(os.environ.get("RICHUP_CAPTCHA_TIMEOUT", "90"))
# IPv6-only challenge host -> Cloudflare IPv4 edge (overridable)
BRUNHILD_IP = os.environ.get("RICHUP_BRUNHILD_IP", "104.18.94.41")

# language=javascript — evaluated in the page; renders a fresh widget and
# resolves with the token (or rejects with the error code).
_RENDER_JS = """
([sitekey]) => new Promise((resolve, reject) => {
    try {
        const holder = document.createElement('div');
        holder.style.cssText =
            'position:fixed;right:8px;bottom:8px;width:300px;height:65px;z-index:2147483647';
        document.body.appendChild(holder);
        window.turnstile.render(holder, {
            sitekey,
            callback: (t) => { holder.remove(); resolve(t); },
            'error-callback': (e) => { holder.remove(); reject(new Error('turnstile-error:' + e)); },
            'timeout-callback': () => { holder.remove(); reject(new Error('turnstile-timeout')); },
            'expired-callback': () => { holder.remove(); reject(new Error('turnstile-expired')); },
        });
    } catch (e) {
        reject(e);
    }
})
"""


def _fetch_api_js() -> str:
    """Fetch the Turnstile api.js source for in-page eval injection.

    challenges.cloudflare.com can resolve IPv6-only here while the machine
    has no IPv6 route -> force AF_INET for this lookup and retry blips.
    """
    req = urllib.request.Request(TURNSTILE_API,
                                 headers={"User-Agent": "Mozilla/5.0"})
    orig = socket.getaddrinfo

    def _ipv4(host, port, family=0, *a, **kw):
        return orig(host, port, socket.AF_INET, *a, **kw)

    last: Exception | None = None
    for _ in range(4):
        try:
            socket.getaddrinfo = _ipv4
            return urllib.request.urlopen(req, timeout=20).read().decode("utf-8")
        except Exception as e:
            last = e
            time.sleep(0.8)
        finally:
            socket.getaddrinfo = orig
    raise last  # type: ignore[misc]


class TurnstileProvider:
    """Owns one real-Chrome page parked on richup.io that mints tokens."""

    def __init__(self, base_url: str = "https://richup.io", headless: bool | None = None):
        self.base_url = base_url.rstrip("/")
        if headless is None:
            headless = os.environ.get("RICHUP_CAPTCHA_HEADLESS", "0") == "1"
        self.headless = headless
        self._pw = None
        self._browser = None
        self._ctx = None
        self._page = None
        self._lock = asyncio.Lock()
        self._started = asyncio.Event()

    async def start(self) -> None:
        if self._started.is_set():
            return
        try:
            from patchright.async_api import async_playwright
        except ImportError:
            from playwright.async_api import async_playwright  # fallback

        self._pw = await async_playwright().start()
        launch_kwargs: dict = {
            "headless": self.headless,
            "args": [
                "--no-first-run",
                "--disable-dev-shm-usage",
                f"--host-resolver-rules=MAP brunhild.challenges.cloudflare.com {BRUNHILD_IP}",
            ],
        }
        try:
            self._browser = await self._pw.chromium.launch(channel="chrome", **launch_kwargs)
        except Exception:
            log.warning("channel='chrome' unavailable; using bundled chromium")
            self._browser = await self._pw.chromium.launch(**launch_kwargs)
        self._ctx = await self._browser.new_context(viewport={"width": 1366, "height": 768})
        self._page = await self._ctx.new_page()
        await self._page.goto(self.base_url + "/", wait_until="domcontentloaded")
        await self._page.wait_for_timeout(2500)

        if await self._page.evaluate("typeof window.turnstile") != "object":
            api_src = await asyncio.to_thread(_fetch_api_js)
            await self._page.evaluate(
                """(src) => {
                    window.onloadTurnstileCallback = () => { window.__tsReady = true; };
                    try { (0, eval)(src); } catch (e) { window.__tsErr = String(e); }
                }""",
                api_src,
            )
            # give the api a moment to self-initialize
            for _ in range(30):
                if await self._page.evaluate("typeof window.turnstile") == "object":
                    break
                await self._page.wait_for_timeout(500)
        if await self._page.evaluate("typeof window.turnstile") != "object":
            raise RuntimeError("turnstile api.js failed to initialize in the page")
        self._started.set()
        log.info("turnstile provider ready (headless=%s)", self.headless)

    async def get_token(self) -> str:
        """Mint a fresh single-use token. Serialized across callers.

        Cloudflare occasionally stalls a widget (no callback at all); retry
        with a fresh widget a few times before giving up. If the browser
        itself dies (user closed the window, TargetClosed), relaunch it.
        """
        last_boot: Exception | None = None
        for boot in range(3):
            try:
                await self.start()
                break
            except Exception as e:
                last_boot = e
                log.warning("turnstile start failed (%d/3): %s", boot + 1, e)
            await self.close()
            await asyncio.sleep(1.5)
        else:
            raise RuntimeError(f"turnstile provider failed to start: {last_boot}")
        async with self._lock:
            last_err: Exception | None = None
            for attempt in range(3):
                try:
                    token = await asyncio.wait_for(
                        self._page.evaluate(_RENDER_JS, [SITEKEY]),
                        timeout=TOKEN_TIMEOUT_S,
                    )
                    if token and isinstance(token, str):
                        return token
                    last_err = RuntimeError("turnstile returned empty token")
                except Exception as e:
                    last_err = e
                    log.warning("token mint attempt %d failed: %s", attempt + 1, e)
            raise RuntimeError(f"turnstile token mint failed: {last_err}")

    async def close(self) -> None:
        try:
            if self._browser:
                await self._browser.close()
            if self._pw:
                await self._pw.stop()
        except Exception:
            pass
        self._browser = self._ctx = self._page = self._pw = None
        self._started.clear()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, *exc):
        await self.close()


_shared: TurnstileProvider | None = None


async def shared_provider() -> TurnstileProvider:
    global _shared
    if _shared is None:
        _shared = TurnstileProvider()
        await _shared.start()
    return _shared
