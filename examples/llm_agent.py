"""LLM agent for richup-bench over any OpenAI-compatible chat API.

Works with:
  - OpenRouter   (https://openrouter.ai/api/v1, key = OPENROUTER_API_KEY)
  - OpenAI       (https://api.openai.com/v1,   key = OPENAI_API_KEY)
  - vLLM/Ollama/LM Studio (any local OpenAI-compatible server)

Swap models with --model, e.g.:
    python examples/llm_agent.py --model anthropic/claude-sonnet-4
    python examples/llm_agent.py --model openai/gpt-4o-mini --play 4
    python examples/llm_agent.py --base-url http://localhost:11434/v1 \
        --model llama3.1 --api-key none

The harness clamps decide() to the live turn clock — if the model doesn't
answer in time it plays the safe default instead of eating a strike.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import re
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from richup.harness import AgentHarness  # noqa: E402

log = logging.getLogger("llm-agent")

SYSTEM = """\
You are playing RichUp, an online Monopoly-like board game, against other \
players (humans and bots). Each message shows the board state; pick ONE \
action from the available list and reply with JSON only:

{"action": "<name>", "args": {...}, "note": "<one short sentence>"}

args for actions that need them (all others take NONE — omit "args"):
  sell_property/upgrade_city/downgrade_city -> {"block_index": N}
  mortgage_property/lift_mortgage -> {"property_index": N}
  auction_bid -> {"amount": N}
  chat -> {"content": "..."}
  create_trade -> {"trade": {"initiatorId": "<you>", "recipientId": "<them>",
      "initiatorOffer": {"money": N, "properties": [blockIndex,...]},
      "recipientOffer": {"money": N, "properties": [...]}}}
  decline_trade/confirm_trade/delete_trade -> {"trade_id": "..."}
IMPORTANT: buy_property and start_auction take NO args — they act on the
unowned block you are standing on. roll_dice and end_turn take no args.

Strategy: when you land on an unowned property, buy_property is almost \
always the right move if you can afford it — unbought land earns nothing. \
Keep ~$100 buffer. Complete color sets, then build houses evenly. In \
prison try rolling doubles before paying. The "clock:" line is your turn \
deadline — when it says URGENT, act immediately with the simplest legal \
move (usually roll_dice or end_turn)."""

# map common model phrasings onto our action names
_ALIASES = {
    "roll": "roll_dice", "roll_dice": "roll_dice", "roll_dices": "roll_dice",
    "end": "end_turn", "end_turn": "end_turn", "pass": "end_turn",
    "buy": "buy_property", "buy_property": "buy_property",
    "purchase": "buy_property", "purchase_property": "buy_property",
    "auction": "start_auction", "start_auction": "start_auction",
    "bid": "auction_bid", "auction_bid": "auction_bid",
    "sell": "sell_property", "sell_property": "sell_property",
    "upgrade": "upgrade_city", "upgrade_city": "upgrade_city",
    "build": "upgrade_city", "downgrade_city": "downgrade_city",
    "mortgage": "mortgage_property", "mortgage_property": "mortgage_property",
    "unmortgage": "lift_mortgage", "lift_mortgage": "lift_mortgage",
    "lift_property_mortgage": "lift_mortgage",
    "pay": "pay_out_of_prison", "pay_out_of_prison": "pay_out_of_prison",
    "pardon": "use_pardon_card", "use_pardon_card": "use_pardon_card",
    "wait": "wait", "nothing": "wait", "observe": "wait", "no_op": "wait",
    "request_clock_time": "request_clock_time",
    "grant_clock_time": "grant_clock_time",
    "chat": "chat", "send_message": "chat",
    "create_trade": "create_trade", "trade": "create_trade",
    "confirm_trade": "confirm_trade", "accept_trade": "confirm_trade",
    "decline_trade": "decline_trade", "reject_trade": "decline_trade",
    "delete_trade": "delete_trade",
}

_JSON_RE = re.compile(r"\{.*\}", re.S)


class LLMAgent:
    """decide() -> one chat completion -> parsed action dict."""

    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        base_url: str = "https://openrouter.ai/api/v1",
        http_timeout_s: float = 45.0,
        max_tokens: int = 220,
        temperature: float = 0.3,
        keep_history: int = 0,
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or "none"
        self.http_timeout_s = http_timeout_s
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.keep_history = keep_history      # past decisions to echo back
        self._http: httpx.AsyncClient | None = None
        self._history: list[dict] = []
        self.calls = 0
        self.parse_failures = 0

    def _client(self) -> httpx.AsyncClient:
        if self._http is None:
            self._http = httpx.AsyncClient(timeout=self.http_timeout_s)
        return self._http

    async def decide(self, obs: dict) -> dict:
        s = obs["state"]
        user = self._prompt(obs)
        msgs = [{"role": "system", "content": SYSTEM}]
        msgs += self._history[-self.keep_history:] if self.keep_history else []
        msgs.append({"role": "user", "content": user})
        headers = {"Authorization": f"Bearer {self.api_key}"}
        if "openrouter" in self.base_url:
            headers["HTTP-Referer"] = "https://github.com/richup-bench"
            headers["X-Title"] = "richup-bench"
        r = await self._client().post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json={
                "model": self.model,
                "messages": msgs,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
            },
        )
        r.raise_for_status()
        text = r.json()["choices"][0]["message"]["content"] or ""
        self.calls += 1
        decision = self._parse(text, set(obs["available_actions"]))
        if self.keep_history:
            self._history.append({"role": "assistant", "content": text})
            self._history.append({"role": "user", "content":
                                  f"(played {decision['action']})"})
        log.info("LLM -> %s %s | %s", decision["action"],
                 decision.get("args") or "", text.strip()[:120])
        return decision

    # ---------------------------------------------------------------- prompt
    def _prompt(self, obs: dict) -> str:
        s = obs["state"]
        lines = [obs["board"]]
        evs = [e for e in obs["new_events"]
               if e.get("event") not in ("sync-game-state",)]
        if evs:
            lines.append("new events: " + "; ".join(
                f"{e['event']} {json.dumps(e.get('data') or {}, default=str)[:160]}"
                for e in evs[-6:]))
        lines.append("available actions: " + ", ".join(
            a for a in obs["available_actions"] if a != "sync"))
        # make the buy decision salient — models were blind-ending turns
        if "buy_property" in obs["available_actions"]:
            pos = (s.get("self") or {}).get("position")
            blocks = s.get("blocks") or []
            if isinstance(pos, int) and 0 <= pos < len(blocks):
                b = blocks[pos]
                lines.append(
                    f"OPPORTUNITY: you are standing on unowned "
                    f"{b.get('name')} — buy_property takes it for "
                    f"${b.get('price')} (you have ${(s.get('self') or {}).get('money')}).")
        clk = s.get("clock") or {}
        if clk.get("turnExpiresInMs") is not None and \
                (s.get("turn") or {}).get("isMyTurn"):
            lines.append(
                f"TURN CLOCK: {max(0, clk['turnExpiresInMs'] / 1000):.0f}s "
                f"to act or the server acts for you "
                f"(strikes {clk.get('myAutoActedTurns', 0)}/"
                f"{clk.get('removalAfterAutoActedTurns', 2)}).")
        return "\n".join(lines)

    # ----------------------------------------------------------------- parse
    def _parse(self, text: str, acts: set[str]) -> dict:
        m = _JSON_RE.search(text)
        data: dict = {}
        if m:
            try:
                data = json.loads(m.group(0))
            except json.JSONDecodeError:
                pass
        raw = str(data.get("action", "")).strip().lower().replace(" ", "_")
        action = _ALIASES.get(raw, raw if raw in acts else "")
        args = data.get("args") or data.get("arguments") or {}
        if not isinstance(args, dict):
            args = {}
        if action and action in acts:
            return {"action": action, "args": args}
        # salvage: regex an action name straight out of the text
        low = text.lower()
        for a in ("roll_dice", "end_turn", "buy_property", "auction_bid",
                  "pay_out_of_prison", "use_pardon_card"):
            if a in acts and (a in low or a.replace("_", " ") in low):
                self.parse_failures += 1
                return {"action": a, "args": {}}
        self.parse_failures += 1
        # last resort: safest available move
        for a in ("roll_dice", "end_turn", "wait"):
            if a in acts or a == "wait":
                return {"action": a, "args": {}}
        return {"action": "wait", "args": {}}


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="openai/gpt-4o-mini",
                    help="model id on the provider (OpenRouter slug etc.)")
    ap.add_argument("--base-url", default="https://openrouter.ai/api/v1")
    ap.add_argument("--api-key", default=None,
                    help="defaults to $OPENROUTER_API_KEY or $OPENAI_API_KEY")
    ap.add_argument("--name", default=None, help="seat name (default: model)")
    ap.add_argument("--room", default=None, help="join existing room id")
    ap.add_argument("--code", default=None, help="join by share code")
    ap.add_argument("--play", type=int, default=None, metavar="N",
                    help="matchmake a public N-player room")
    ap.add_argument("--appearance", default="#5A99DA")
    ap.add_argument("--trace", default=None, help="JSONL trace path")
    ap.add_argument("--public", dest="private", action="store_false")
    ap.add_argument("--decision-timeout", type=float, default=60.0,
                    help="max seconds per decide() before the safe fallback")
    ap.add_argument("--start-timeout", type=float, default=1800,
                    help="max seconds to wait in the lobby for the game")
    ap.add_argument("--max-tokens", type=int, default=220)
    ap.add_argument("--history", type=int, default=0,
                    help="assistant turns to resend each call")
    ap.add_argument("--settings", default=None,
                    help='JSON room settings, e.g. \'{"maxPlayers":2}\'')
    ap.add_argument("--no-bots", dest="fill_bots", action="store_false",
                    help="don't auto-fill empty seats with bots")
    ap.add_argument("--captcha-token", default=None)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    api_key = args.api_key or os.environ.get("OPENROUTER_API_KEY") \
        or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        ap.error("no API key: pass --api-key or set OPENROUTER_API_KEY")

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(name)s %(message)s")
    name = args.name or args.model.split("/")[-1][:20]
    agent = LLMAgent(model=args.model, api_key=api_key,
                     base_url=args.base_url, max_tokens=args.max_tokens,
                     keep_history=args.history)
    harness = AgentHarness(agent, name=name, appearance=args.appearance,
                           trace_path=args.trace,
                           captcha_token=args.captcha_token,
                           verbose=args.verbose,
                           decision_timeout_s=args.decision_timeout)
    result = await harness.run(room_id=args.room, room_code=args.code,
                               quick_play=args.play,
                               settings=json.loads(args.settings)
                               if args.settings else None,
                               fill_bots=args.fill_bots,
                               is_private=args.private,
                               start_timeout_s=args.start_timeout)
    result["llm_calls"] = agent.calls
    result["parse_failures"] = agent.parse_failures
    print("EPISODE RESULT:", result)


if __name__ == "__main__":
    asyncio.run(main())
