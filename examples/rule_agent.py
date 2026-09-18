"""Example rule-based agent for richup-bench.

Baseline policy:
  - in prison            -> pay out (or use pardon card if we hold one)
  - my turn, not rolled  -> roll_dice
  - landed on unowned    -> buy if affordable (keep a cash buffer), else auction
  - auction running      -> bid up to 60% of face value while affordable
  - flush with cash      -> upgrade cheapest owned city (even build)
  - incoming trades      -> decline (bots rarely offer fair trades)
  - otherwise            -> end_turn / wait

Run:
    python examples/rule_agent.py [--name BenchBot] [--room ID] [--trace out.jsonl]
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from richup.harness import AgentHarness

log = logging.getLogger("rule-agent")

CASH_BUFFER = 100        # never spend below this reserve
AUCTION_MAX_RATIO = 0.6  # bid up to this fraction of face value


class RuleAgent:
    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)
        self._acted_this_turn = False

    async def decide(self, obs: dict) -> dict:
        s = obs["state"]
        acts = set(obs["available_actions"])
        turn = s["turn"]
        me = s["self"]
        gs_money = me.get("money") or 0
        auction = s.get("auction")

        # --- auctions happen off-turn too -----------------------------------
        if auction and "auction_bid" in acts:
            cur = auction.get("currentBid") or auction.get("price") or 0
            face = (auction.get("block") or {}).get("price") or 200
            cap = int(face * AUCTION_MAX_RATIO)
            if gs_money - CASH_BUFFER > cur + 10 and cur + 10 <= cap:
                return {"action": "auction_bid", "args": {"amount": cur + 10}}
            return {"action": "wait"}

        # --- trades: decline anything offered to us --------------------------
        for tr in s.get("trades") or []:
            if tr.get("recipientId") == me.get("playerId") \
                    and "decline_trade" in acts:
                return {"action": "decline_trade",
                        "args": {"trade_id": tr.get("id")}}

        if not turn["isMyTurn"]:
            self._acted_this_turn = False
            return {"action": "wait"}

        # --- my turn ----------------------------------------------------------
        imprisoned = me.get("inPrison")
        if imprisoned and "roll_dice" in acts:
            return {"action": "roll_dice"}        # try doubles for free escape
        if "pay_out_of_prison" in acts:
            return {"action": "pay_out_of_prison"}
        if "use_pardon_card" in acts:
            return {"action": "use_pardon_card"}

        if "roll_dice" in acts:
            return {"action": "roll_dice"}

        # after rolling: maybe buy / build / end
        if "buy_property" in acts:
            price = _landed_price(obs)
            if price is None or gs_money - price >= CASH_BUFFER:
                return {"action": "buy_property"}
            # can't afford: auction it off if the room allows, else pass
            if "start_auction" in acts:
                return {"action": "start_auction"}
            return {"action": "end_turn"}

        # build houses when rich (cheapest city first keeps evenBuild happy)
        if "upgrade_city" in acts and gs_money > 700 and self.rng.random() < 0.3:
            idx = _cheapest_city(obs)
            if idx is not None:
                return {"action": "upgrade_city", "args": {"block_index": idx}}

        if "end_turn" in acts:
            return {"action": "end_turn"}
        return {"action": "wait"}


def _landed_price(obs: dict) -> int | None:
    """Price of the block we're on (None if not purchasable)."""
    s = obs["state"]
    blocks = s.get("blocks") or []
    pos = (s.get("self") or {}).get("position")
    if pos is None or not (0 <= pos < len(blocks)):
        return None
    b = blocks[pos]
    if b.get("ownerId") is not None or b.get("price") is None:
        return None
    return b["price"]


def _cheapest_city(obs: dict) -> int | None:
    s = obs["state"]
    me_id = s["self"]["playerId"]
    mine = next((p for p in s["players"] if p.get("id") == me_id), None)
    cities = [pr for pr in (mine or {}).get("properties", []) if pr.get("type") == "city"]
    if not cities:
        return None
    cities.sort(key=lambda pr: (pr.get("level") or 0, pr["index"]))
    return cities[0]["index"]


async def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="RuleBot")
    ap.add_argument("--room", default=None, help="join existing room id")
    ap.add_argument("--code", default=None,
                    help="join by share code (e.g. X4SF7)")
    ap.add_argument("--play", type=int, default=None, metavar="N",
                    help="'Play' button: matchmake a public N-player room")
    ap.add_argument("--appearance", default="#5A99DA")
    ap.add_argument("--trace", default=None, help="JSONL trace path")
    ap.add_argument("--private", action="store_true", default=True)
    ap.add_argument("--public", dest="private", action="store_false")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--captcha-token", default=None,
                    help="manually-solved Turnstile token (single use)")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(name)s %(message)s")
    agent = RuleAgent()
    harness = AgentHarness(agent, name=args.name, appearance=args.appearance,
                           trace_path=args.trace,
                           captcha_token=args.captcha_token,
                           verbose=args.verbose)
    result = await harness.run(room_id=args.room, room_code=args.code,
                               quick_play=args.play,
                               is_private=args.private)
    print("EPISODE RESULT:", result)


if __name__ == "__main__":
    asyncio.run(main())
