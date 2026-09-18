"""Agent harness: run an episode of richup.io for a pluggable agent.

The agent implements one method:

    async def decide(self, obs: dict) -> dict | None

`obs` = {"state": summarize(...), "board": render(...),
         "available_actions": [...], "new_events": [...]}
Return {"action": "<action name>", "args": {...}} to act, or None/"wait"
to observe only. Action names map to RichUpClient methods (ACTIONS below).

Every observation, action, ack and error is appended to a JSONL trace so
episodes can be scored/replayed offline.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from . import events as ev
from . import state as st
from .client import ActionError, RichUpClient
from .session import GameSession

log = logging.getLogger("richup.harness")

# action name -> client method name (agent-facing vocabulary)
ACTIONS: dict[str, str] = {
    "wait": "",
    "roll_dice": "roll_dice",
    "end_turn": "end_turn",
    "pay_out_of_prison": "pay_out_of_prison",
    "use_pardon_card": "use_pardon_card",
    "buy_property": "buy_property",
    "sell_property": "sell_property",
    "upgrade_city": "upgrade_city",
    "downgrade_city": "downgrade_city",
    "mortgage_property": "mortgage_property",
    "lift_mortgage": "lift_mortgage",
    "start_auction": "start_auction",
    "auction_bid": "auction_bid",
    "create_trade": "create_trade",
    "confirm_trade": "confirm_trade",
    "decline_trade": "decline_trade",
    "delete_trade": "delete_trade",
    "chat": "chat",
    "bankrupt": "bankrupt",
    "request_clock_time": "request_clock_time",
    "grant_clock_time": "grant_clock_time",
    "votekick": "votekick",
    "host_kick": "host_kick",
    "start_game": "start_game",
    "update_game_room": "update_game_room",
    "sync": "sync",
}

ARG_NAMES: dict[str, tuple[str, ...]] = {
    "sell_property": ("block_index",),
    "upgrade_city": ("block_index",),
    "downgrade_city": ("block_index",),
    "mortgage_property": ("property_index",),
    "lift_mortgage": ("property_index",),
    "auction_bid": ("amount",),
    "create_trade": ("trade", "negotiated_trade_id"),
    "confirm_trade": ("trade_id",),
    "decline_trade": ("trade_id",),
    "delete_trade": ("trade_id",),
    "chat": ("content",),
    "votekick": ("player_id",),
    "host_kick": ("player_id",),
}


class Trace:
    """JSONL episode recorder."""

    def __init__(self, path: str | Path | None):
        self.path = Path(path) if path else None
        self._fh = self.path.open("a") if self.path else None

    def write(self, kind: str, data: Any) -> None:
        rec = {"t": time.time(), "kind": kind, "data": data}
        if self._fh:
            self._fh.write(json.dumps(rec, default=str) + "\n")
            self._fh.flush()

    def close(self) -> None:
        if self._fh:
            self._fh.close()


async def dispatch(client: RichUpClient, action: str, args: dict | None) -> Any:
    """Map an agent action to a client call. Returns ack or {'error':...}."""
    if action in ("wait", None, ""):
        return {"ok": True, "waited": True}
    method_name = ACTIONS.get(action)
    if method_name is None:
        return {"ok": False, "error": f"unknown action {action!r}",
                "valid": sorted(ACTIONS)}
    fn: Callable = getattr(client, method_name)
    args = dict(args or {})
    # accept both positional-by-name and exact kwargs
    names = ARG_NAMES.get(action, ())
    positional = [args.pop(n) for n in names if n in args]
    if action == "update_game_room":
        return await fn(**args)
    if action == "create_trade":
        return await fn(*positional, **args)
    return await fn(*positional, **args)


class AgentHarness:
    """Runs one seat in one room for one agent."""

    def __init__(
        self,
        agent,
        name: str = "Agent",
        appearance: str = "#5A99DA",
        base_url: str = "https://richup.io",
        trace_path: str | None = None,
        poll_s: float = 0.7,
        captcha_token: str | None = None,
        verbose: bool = False,
        decision_timeout_s: float | None = 60.0,
        clock_margin_ms: int = 6000,
        auto_grant_clock: bool = True,
        auto_request_clock: bool = True,
        auto_request_below_ms: int = 15000,
    ):
        self.agent = agent
        self.session = GameSession(name=name, appearance=appearance,
                                   base_url=base_url,
                                   captcha_token=captcha_token,
                                   verbose=verbose)
        self.trace = Trace(trace_path)
        self.poll_s = poll_s
        self._cursor = 0
        # --- turn-clock management -----------------------------------------
        # RichUp gives ~20s grace per turn, then drains the player's time
        # bank; expiry => server auto-acts, 2 strikes => removal.
        # decision_timeout_s bounds a single decide() call (None = never).
        # The effective bound is min(decision_timeout_s, timeLeft-margin):
        # if the agent can't answer before the clock dies, we take the
        # server's own default action instead of eating a strike.
        self.decision_timeout_s = decision_timeout_s
        self.clock_margin_ms = clock_margin_ms
        self.auto_grant_clock = auto_grant_clock      # grant when others ask
        self.auto_request_clock = auto_request_clock  # ask when our clock low
        self.auto_request_below_ms = auto_request_below_ms
        self._clock_requested_turn: int | None = None
        self.timeout_fallbacks = 0

    # ------------------------------------------------------------------ obs
    def _observation(self) -> dict:
        c = self.session.client
        evs = list(c.events)
        new = evs[self._cursor:]
        self._cursor = len(evs)
        return {
            "state": st.summarize(c),
            "board": st.render(c, recent_events=0),
            "available_actions": st.available_actions(c),
            "new_events": new,
        }

    # --------------------------------------------------------------- clock
    def _removed_from_game(self) -> bool:
        """We were auto-removed (2 strikes) or lost our seat."""
        c = self.session.client
        gs = c.game_state or {}
        if gs.get("phase") != "playing" or not c.self_player_id:
            return False
        return st.find_player(gs, c.self_player_id) is None

    def _clock_fallback(self) -> str | None:
        """If my turn clock is inside the safety margin, return the server's
        own default action (roll if unrolled else end-turn)."""
        c = self.session.client
        s = st.summarize(c)
        t = s.get("turn") or {}
        clk = s.get("clock") or {}
        if not t.get("isMyTurn"):
            return None
        left = clk.get("turnExpiresInMs")
        if left is None or left > self.clock_margin_ms:
            return None
        return "roll_dice" if not t.get("cubesRolledInTurn") else "end_turn"

    def _decision_deadline_s(self) -> float | None:
        """min(decision_timeout_s, turnClock budget minus margin)."""
        budget = self.decision_timeout_s
        c = self.session.client
        s = st.summarize(c)
        t = s.get("turn") or {}
        clk = s.get("clock") or {}
        if t.get("isMyTurn") and clk.get("turnExpiresInMs") is not None:
            clock_budget = max(
                0.0, (clk["turnExpiresInMs"] - self.clock_margin_ms) / 1000)
            budget = clock_budget if budget is None else min(budget,
                                                             clock_budget)
        return budget

    async def _clock_housekeeping(self, obs: dict) -> None:
        c = self.session.client
        # grant time to anyone else who asked (keeps all-agent tables alive)
        if self.auto_grant_clock:
            for e in obs["new_events"]:
                if e.get("event") != ev.CLOCK_TIME_REQUESTED:
                    continue
                d = e.get("data") or {}
                pid = d.get("participantId") or d.get("playerId")
                if pid == c.self_player_id:
                    continue
                try:
                    await c.grant_clock_time()
                    log.info("granted clock time (requested by %s)", pid)
                except ActionError as ex:
                    log.debug("grant_clock_time: %s", ex)
                break
        # ask for time when our own clock is running low (once per turn)
        s = obs.get("state") or {}
        t = s.get("turn") or {}
        clk = s.get("clock") or {}
        if (self.auto_request_clock and t.get("isMyTurn")
                and (clk.get("turnExpiresInMs") or 0)
                < self.auto_request_below_ms):
            gs = c.game_state or {}
            tid = ((gs.get("turnClock") or {}).get("turn") or {}) \
                .get("turnStartedAt")
            if tid is not None and tid != self._clock_requested_turn:
                self._clock_requested_turn = tid
                try:
                    await c.request_clock_time()
                    log.info("clock low (%dms) — requested clock time",
                             clk["turnExpiresInMs"])
                except ActionError as ex:
                    log.debug("request_clock_time: %s", ex)

    # ------------------------------------------------------------------ run
    async def run(
        self,
        room_id: str | None = None,
        room_code: str | None = None,
        quick_play: int | None = None,
        settings: dict | None = None,
        fill_bots: bool = True,
        min_players: int = 2,
        max_steps: int = 4000,
        is_private: bool = True,
        wait_for_start: bool = True,
        start_timeout_s: float | None = 1800,
    ) -> dict:
        """Full episode: create/join -> start -> play until game-ended.

        Entry modes (pick one): room_id | room_code | quick_play=N |
        none (create a fresh private room).
        Returns {"room_id", "winner_id", "steps", "me"}.
        """
        c = self.session.client
        try:
            if room_code:
                room_id = await self.session.join_by_code(room_code)
            elif quick_play:
                room_id = await self.session.quick_play(quick_play)
            elif room_id:
                await self.session.join_existing(room_id)
            else:
                room_id = await self.session.create_and_join(
                    is_private=is_private, settings=settings)
            self.trace.write("joined", {"room_id": room_id,
                                        "player_id": c.self_player_id})
            log.info("joined room %s as %s", room_id, c.self_player_id)

            # host-only actions are tolerated failures when we joined
            # someone else's room (quick_play/room_code joins).
            if fill_bots:
                try:
                    await c.update_game_room(canBotsJoin=True)
                except ActionError:
                    pass
            await self.session.wait_for_players(min_players=min_players,
                                                timeout=90)
            try:
                await c.start_game()
            except ActionError as e:
                log.info("start_game: %s (waiting for host to start)", e)
            if wait_for_start:
                try:
                    await asyncio.wait_for(c.game_started.wait(),
                                           timeout=start_timeout_s)
                except TimeoutError:
                    log.warning("game did not start within %ss; leaving",
                                start_timeout_s)
                    return {"room_id": room_id, "aborted": "start_timeout",
                            "steps": 0, "me": c.self_player_id}
                await c.sync()

            steps = 0
            removed = False
            while not c.game_ended.is_set() and steps < max_steps:
                if self._removed_from_game():
                    removed = True
                    log.warning("removed from game (turn-clock strikes)")
                    self.trace.write("removed", {"reason": "turn-clock"})
                    break
                obs = self._observation()
                self.trace.write("observation", obs["state"])
                await self._clock_housekeeping(obs)
                # urgent: clock nearly dead -> take the safe default now
                fallback = self._clock_fallback()
                decision = None
                if fallback:
                    decision = {"action": fallback}
                    self.timeout_fallbacks += 1
                    self.trace.write("clock_fallback", {"action": fallback})
                    log.info("clock critical -> fallback %s", fallback)
                else:
                    try:
                        deadline = self._decision_deadline_s()
                        if deadline is None:
                            decision = await self.agent.decide(obs)
                        else:
                            decision = await asyncio.wait_for(
                                self.agent.decide(obs), timeout=deadline)
                    except TimeoutError:
                        fallback = self._clock_fallback()
                        decision = {"action": fallback or "wait"}
                        self.timeout_fallbacks += 1
                        self.trace.write("decision_timeout", {
                            "deadline_s": deadline, "fallback": fallback})
                        log.info("decide() exceeded %.1fs -> %s",
                                 deadline, fallback or "wait")
                    except Exception as e:
                        log.warning("agent decide() raised: %s", e)
                action = (decision or {}).get("action", "wait")
                args = (decision or {}).get("args", {})
                result = None
                if action not in (None, "wait"):
                    try:
                        result = await dispatch(c, action, args)
                    except ActionError as e:
                        result = {"ok": False, "code": e.code, "error": str(e)}
                    except Exception as e:
                        result = {"ok": False, "error": str(e)}
                self.trace.write("action", {
                    "action": action, "args": args, "result": result})
                steps += 1
                await asyncio.sleep(self.poll_s)

            end = {"room_id": room_id,
                   "winner_id": (c.game_end_payload or {}).get("winnerId"),
                   "steps": steps,
                   "removed": removed,
                   "timeout_fallbacks": self.timeout_fallbacks,
                   "me": c.self_player_id}
            self.trace.write("ended", end)
            return end
        finally:
            self.trace.close()
            await self.session.close()
