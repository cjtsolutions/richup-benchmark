"""High-level game session: session -> room -> join (captcha) -> bots -> start.

This is the bootstrap layer the MCP server and the agent harness share.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Self

from .captcha import TurnstileProvider
from .client import ActionError, RichUpClient

log = logging.getLogger("richup.session")

APPEARANCE_PALETTE = [
    "#C0DA5A", "#FFC73F", "#FF843F", "#C34848", "#5A99DA", "#7FE7F5",
    "#009688", "#73E85D", "#9A6E5E", "#C63FA2", "#FF7CA0", "#7F5ADA",
]


class GameSession:
    """One client seated in one room. Owns the captcha bootstrap."""

    def __init__(
        self,
        name: str,
        appearance: str = "#5A99DA",
        base_url: str = "https://richup.io",
        captcha_provider: TurnstileProvider | None = None,
        captcha_token: str | None = None,
        verbose: bool = False,
    ):
        if appearance not in APPEARANCE_PALETTE:
            log.warning("appearance %r not in default palette; join may fail", appearance)
        self.name = name
        self.appearance = appearance
        self.client = RichUpClient(base_url=base_url, verbose=verbose)
        self._captcha = captcha_provider
        self._captcha_token = captcha_token
        self._owns_captcha = captcha_provider is None

    # ------------------------------------------------------------------ join
    async def create_and_join(
        self,
        is_private: bool = True,
        settings: dict | None = None,
    ) -> str:
        """Create a room, enter it, join as a player. Returns room_id."""
        await self.client.init_session()
        room_id = await self.client.create_room(is_private=is_private)
        await self._enter_and_join(room_id)
        if settings:
            await self.client.update_game_room(**settings)
        return room_id

    async def join_existing(self, room_id: str) -> None:
        await self.client.init_session()
        await self._enter_and_join(room_id)

    async def join_by_code(self, code: str) -> str:
        """Resolve a share code (e.g. 'X4SF7') to a room and join. Returns room_id."""
        await self.client.init_session()
        room_id = await self.client.find_room(code)
        await self._enter_and_join(room_id)
        return room_id

    async def quick_play(self, max_players: int = 4) -> str:
        """The 'Play' button: /room/find/{2|3|4} matchmakes into a public room."""
        return await self.join_by_code(str(max_players))

    async def _enter_and_join(self, room_id: str) -> None:
        c = self.client
        await c.connect()
        await c.enter_room(room_id)
        token = await self._token()
        try:
            await c.join_game(self.name, appearance=self.appearance,
                              captcha_token=token)
        except ActionError as e:
            raise RuntimeError(f"join-game rejected: {e.code}: {e}") from e

    async def _token(self) -> str:
        # precedence: explicit token > env var > mint via browser
        import os
        if self._captcha_token:
            tok, self._captcha_token = self._captcha_token, None
            return tok
        env_tok = os.environ.pop("RICHUP_CAPTCHA_TOKEN", None)
        if env_tok:
            return env_tok
        if self._captcha is None:
            self._captcha = TurnstileProvider(base_url=self.client.base_url)
        return await self._captcha.get_token()

    # ------------------------------------------------------------------ lobby
    async def wait_for_players(self, min_players: int = 2, timeout: float = 60) -> int:
        """Wait until >= min_players participants are seated. Returns count."""
        deadline = asyncio.get_running_loop().time() + timeout
        while True:
            n = len(self.client.participants)
            if n >= min_players:
                return n
            if asyncio.get_running_loop().time() > deadline:
                return n
            await asyncio.sleep(0.5)

    async def start(
        self,
        fill_bots: bool = True,
        min_players: int = 2,
        wait_s: float = 60,
    ) -> None:
        """Enable bots (optional), wait for seats, start the game."""
        if fill_bots:
            try:
                await self.client.update_game_room(canBotsJoin=True)
            except ActionError as e:
                log.warning("canBotsJoin update failed: %s", e)
        await self.wait_for_players(min_players=min_players, timeout=wait_s)
        await self.client.start_game()
        await asyncio.wait_for(self.client.game_started.wait(), timeout=10)
        await self.client.sync()

    # -------------------------------------------------------------- lifecycle
    async def close(self) -> None:
        await self.client.close()
        if self._owns_captcha and self._captcha is not None:
            await self._captcha.close()
            self._captcha = None

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *exc) -> None:
        await self.close()
