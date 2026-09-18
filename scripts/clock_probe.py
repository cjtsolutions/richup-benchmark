"""Live probe: let a turn expire and observe the auto-act/strike machinery.

Creates a private bot room, starts the game, then on each of our turns:
  turn 1: stall past the clock -> expect auto-act + autoActedTurns=1
  turn 2: act quickly          -> expect strike reset + bank refill
Also pings request_clock_time while stalled to see whether bots grant.
"""

import asyncio
import json
import logging
import sys

sys.path.insert(0, ".")
from richup import state as st
from richup.session import GameSession

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger("clock_probe")


async def main():
    sess = GameSession(name="ClockProbe", appearance="#5A99DA", verbose=True)
    try:
        room = await sess.create_and_join(is_private=True,
                                          settings={"canBotsJoin": True,
                                                    "maxPlayers": 2})
        log.info("room %s", room)
        await sess.wait_for_players(min_players=2, timeout=60)
        await sess.client.start_game()
        await asyncio.wait_for(sess.client.game_started.wait(), 60)
        await sess.client.sync()
        c = sess.client
        stalled = acted = 0
        t_end = asyncio.get_event_loop().time() + 300
        while asyncio.get_event_loop().time() < t_end and stalled < 1:
            gs = c.game_state or {}
            if gs.get("phase") != "playing":
                await asyncio.sleep(1)
                continue
            s = st.summarize(c)
            t = s["turn"]
            clk = s["clock"]
            if t["isMyTurn"]:
                me = st.find_player(gs, c.self_player_id) or {}
                strikes = (me.get("clock") or {}).get("autoActedTurns", 0)
                log.info("MY TURN expires_in=%.0fs strikes=%d bank=%.0fs",
                         clk["turnExpiresInMs"] / 1000, strikes,
                         (clk["myBankMs"] or 0) / 1000)
                if strikes == 0 and stalled == 0:
                    # stall: ask for time at 10s left, else let it expire
                    if 9000 < clk["turnExpiresInMs"] < 12000:
                        try:
                            await c.request_clock_time()
                            log.info(">>> requested clock time")
                        except Exception as e:
                            log.info("request_clock_time: %s", e)
                    if clk["turnExpiresInMs"] < 2000:
                        stalled += 1
                        log.info(">>> let it expire")
                elif acted == 0:
                    # act fast -> should reset strikes & refill bank
                    if not t["cubesRolledInTurn"]:
                        await c.roll_dice()
                    else:
                        await c.end_turn()
                        acted += 1
                        log.info(">>> acted; strikes should reset")
                await asyncio.sleep(1.0)
            else:
                await asyncio.sleep(1.5)
        for e in list(c.events)[-15:]:
            log.info("evt %s %s", e["event"],
                     json.dumps(e["data"], default=str)[:220])
    finally:
        await sess.close()


if __name__ == "__main__":
    asyncio.run(main())
