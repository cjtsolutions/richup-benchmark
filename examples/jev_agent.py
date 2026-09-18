"""Agent for OpenRouter's alpha decisions API (e.g. typesafe/jev-1.13).

JEV-style models don't chat — they answer narrow, typed questions about a
`state` string (`noul` = 0..1 probability, `choice` = distribution over
labels, `score` = distribution over an ordered scale). The harness owns the
workflow: each step we ask ONE choice question over the legal actions,
then at most one follow-up for whatever arg that action needs
(block index, bid amount). Most turns cost exactly one API call.

    python examples/jev_agent.py
    python examples/jev_agent.py --play 4 --model typesafe/jev-1.13

Endpoint: POST {base}/decisions  (default https://openrouter.ai/api/alpha)
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from richup.harness import AgentHarness

log = logging.getLogger("jev-agent")

# actions the typed API can't meaningfully fill args for -> don't offer them
UNOFFERABLE = {"create_trade", "chat", "sync", "wait", "grant_clock_time",
               "host_kick", "votekick", "start_game", "update_game_room",
               "bankrupt"}

ACTION_HELP = {
    "roll_dice": "roll the dice and move",
    "end_turn": "finish your turn",
    "buy_property": "buy the unowned property you are standing on",
    "sell_property": "sell a property back to the bank",
    "upgrade_city": "build a house/hotel on a city you own",
    "downgrade_city": "sell a house/hotel back for cash",
    "mortgage_property": "mortgage a property for cash",
    "lift_mortgage": "pay to unmortgage a property",
    "start_auction": "auction the unowned property you are standing on",
    "auction_bid": "place a bid in the running auction",
    "pay_out_of_prison": "pay bail to leave prison now",
    "use_pardon_card": "use a get-out-of-jail card",
    "request_clock_time": "ask other players for more thinking time",
    "confirm_trade": "accept a pending trade",
    "decline_trade": "reject a pending trade",
    "delete_trade": "withdraw a trade you offered",
}


class JevAgent:
    """decide() -> decisions-API choice -> parsed action dict."""

    def __init__(
        self,
        model: str = "typesafe/jev-1.13",
        api_key: str | None = None,
        base_url: str = "https://openrouter.ai/api/alpha",
        http_timeout_s: float = 45.0,
        site_url: str = "https://github.com/richup-bench",
        site_name: str = "richup-bench",
    ):
        self.model = model
        self.api_key = api_key or ""
        self.decisions_url = f"{base_url.rstrip('/')}/decisions"
        self.site_url = site_url
        self.site_name = site_name
        self.http_timeout_s = http_timeout_s
        self._http: httpx.AsyncClient | None = None
        self.calls = 0
        self.fallbacks = 0

    def _client(self) -> httpx.AsyncClient:
        if self._http is None:
            self._http = httpx.AsyncClient(timeout=self.http_timeout_s)
        return self._http

    async def _ask(self, state: str, questions: dict) -> dict:
        r = await self._client().post(
            self.decisions_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": self.site_url,
                "X-OpenRouter-Title": self.site_name,
            },
            json={"model": self.model, "state": state,
                  "questions": questions},
        )
        r.raise_for_status()
        self.calls += 1
        return (r.json() or {}).get("answers") or {}

    async def decide(self, obs: dict) -> dict:
        s = obs["state"]
        acts = [a for a in obs["available_actions"] if a not in UNOFFERABLE]
        if not acts:
            return {"action": "wait"}
        state_txt = self._state_text(obs)
        criteria = {a: ACTION_HELP.get(a, a) for a in [*acts, "wait"]}
        # make the buy criterion concrete — name + price beat an abstraction
        if "buy_property" in acts:
            pos = (s.get("self") or {}).get("position")
            blocks = s.get("blocks") or []
            if isinstance(pos, int) and 0 <= pos < len(blocks):
                b = blocks[pos]
                criteria["buy_property"] = (
                    f"buy {b.get('name')} for ${b.get('price')} "
                    f"(you have ${(s.get('self') or {}).get('money')}; "
                    f"owning property earns rent)")
        answers = await self._ask(state_txt, {
            "action": {
                "type": "choice",
                "instructions": "You are playing a Monopoly-like board game "
                                "against other players. Pick the single best "
                                "action right now, or 'wait' to observe. "
                                "Buying an unowned property you just landed "
                                "on is almost always the best move — it earns "
                                "rent forever. Only end your turn after "
                                "deciding what to do with the block you "
                                "landed on.",
                "criteria": criteria,
            },
        })
        action = (answers.get("action") or {}).get("choice", "wait")
        probs = (answers.get("action") or {}).get("probabilities") or {}
        log.info("JEV action=%s (p=%.2f) probs=%s", action,
                 probs.get(action, 0.0),
                 {k: round(v, 2) for k, v in
                  sorted(probs.items(), key=lambda kv: -kv[1])[:3]})
        if action not in acts:
            self.fallbacks += 1
            for a in ("roll_dice", "end_turn", "wait"):
                if a in acts or a == "wait":
                    action = a
                    break
        args = {}
        if action in ("sell_property", "upgrade_city", "downgrade_city",
                      "mortgage_property", "lift_mortgage"):
            args = await self._pick_block(state_txt, obs, action)
            if not args:
                action = "wait"     # arg pick cancelled/failed -> don't emit
        elif action == "auction_bid":
            args = await self._pick_bid(state_txt, obs)
            if not args:
                action = "wait"
        elif action in ("confirm_trade", "decline_trade", "delete_trade"):
            tid = self._first_trade_id(obs)
            args = {"trade_id": tid} if tid else {}
            if not tid:
                action = "wait"
        return {"action": action, "args": args}

    # -------------------------------------------------------------- helpers
    def _state_text(self, obs: dict) -> str:
        s = obs["state"]
        lines = [obs["board"]]
        clk = s.get("clock") or {}
        if (s.get("turn") or {}).get("isMyTurn") and \
                clk.get("turnExpiresInMs") is not None:
            lines.append(
                f"Turn clock: {max(0, clk['turnExpiresInMs'] / 1000):.0f}s "
                f"left; {clk.get('myAutoActedTurns', 0)}/"
                f"{clk.get('removalAfterAutoActedTurns', 2)} strikes.")
        evs = [e for e in obs["new_events"]
               if e.get("event") not in ("sync-game-state",)]
        if evs:
            lines.append("Recent: " + "; ".join(
                f"{e['event']}" for e in evs[-6:]))
        return "\n".join(lines)

    async def _pick_block(self, state: str, obs: dict,
                          action: str) -> dict:
        s = obs["state"]
        me = (s.get("self") or {}).get("playerId")
        owned = [p for pl in s.get("players") or [] if pl.get("id") == me
                 for p in pl.get("properties") or []]
        if not owned:
            return {}
        criteria = {
            str(p["index"]): f"{p.get('name', '?')} "
                             f"(level {p.get('level', 0)}"
                             f"{', mortgaged' if p.get('mortgaged') else ''})"
            for p in owned}
        criteria["cancel"] = "don't do this after all"
        answers = await self._ask(state, {
            "block": {"type": "choice",
                      "instructions": f"Which property should we apply "
                                      f"'{action}' to?",
                      "criteria": criteria}})
        pick = (answers.get("block") or {}).get("choice", "cancel")
        try:
            idx = int(pick)
            if action in ("mortgage_property", "lift_mortgage"):
                return {"property_index": idx}
            return {"block_index": idx}
        except ValueError:
            return {}

    async def _pick_bid(self, state: str, obs: dict) -> dict:
        s = obs["state"]
        auct = s.get("auction") or {}
        cur = auct.get("currentBid") or auct.get("price") or 0
        face = ((auct.get("block") or {}).get("price")) or cur + 50
        money = (s.get("self") or {}).get("money") or 0
        options = {str(int(v)): f"bid ${int(v)}"
                   for v in (cur + 10, cur + 25, cur + 50,
                             min(face, money - 100))
                   if cur + 10 <= v <= money - 100}
        if not options:
            return {}
        options["pass"] = "stop bidding"
        answers = await self._ask(state, {
            "bid": {"type": "choice",
                    "instructions": "An auction is running for an unowned "
                                    "property. How much should we bid, if "
                                    "anything?",
                    "criteria": options}})
        pick = (answers.get("bid") or {}).get("choice", "pass")
        try:
            return {"amount": int(pick)} if pick != "pass" else {}
        except ValueError:
            return {}

    def _first_trade_id(self, obs: dict) -> str | None:
        me = (obs["state"].get("self") or {}).get("playerId")
        for tr in obs["state"].get("trades") or []:
            if tr.get("recipientId") == me or tr.get("initiatorId") == me:
                return tr.get("id")
        return None


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="typesafe/jev-1.13")
    ap.add_argument("--base-url", default="https://openrouter.ai/api/alpha",
                    help="alpha API root (we append /decisions)")
    ap.add_argument("--api-key", default=None,
                    help="defaults to $OPENROUTER_API_KEY")
    ap.add_argument("--name", default="Jev")
    ap.add_argument("--room", default=None, help="join existing room id")
    ap.add_argument("--code", default=None, help="join by share code")
    ap.add_argument("--play", type=int, default=None, metavar="N",
                    help="matchmake a public N-player room")
    ap.add_argument("--appearance", default="#5A99DA")
    ap.add_argument("--trace", default=None, help="JSONL trace path")
    ap.add_argument("--decision-timeout", type=float, default=45.0)
    ap.add_argument("--start-timeout", type=float, default=1800,
                    help="max seconds to wait in the lobby for the game")
    ap.add_argument("--settings", default=None,
                    help='JSON room settings, e.g. \'{"maxPlayers":2}\'')
    ap.add_argument("--no-bots", dest="fill_bots", action="store_false",
                    help="don't auto-fill empty seats with bots")
    ap.add_argument("--captcha-token", default=None)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    api_key = args.api_key or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        ap.error("no API key: pass --api-key or set OPENROUTER_API_KEY")

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(name)s %(message)s")
    agent = JevAgent(model=args.model, api_key=api_key,
                     base_url=args.base_url)
    harness = AgentHarness(agent, name=args.name, appearance=args.appearance,
                           trace_path=args.trace,
                           captcha_token=args.captcha_token,
                           verbose=args.verbose,
                           decision_timeout_s=args.decision_timeout)
    result = await harness.run(room_id=args.room, room_code=args.code,
                               quick_play=args.play,
                               settings=json.loads(args.settings)
                               if args.settings else None,
                               fill_bots=args.fill_bots,
                               start_timeout_s=args.start_timeout)
    result["jev_calls"] = agent.calls
    result["fallbacks"] = agent.fallbacks
    print("EPISODE RESULT:", result)


if __name__ == "__main__":
    asyncio.run(main())
