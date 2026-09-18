"""Live end-to-end smoke test:
session -> create room -> enter -> captcha -> join -> allow bots -> start -> play.
"""

import asyncio
import json
import sys

sys.path.insert(0, ".")
from richup.client import RichUpClient, ActionError
from richup.captcha import TurnstileProvider


async def main():
    c = RichUpClient(verbose=False)
    await c.init_session()

    room_id = await c.create_room(is_private=True)
    print("room_id:", room_id)

    async def _p(d):
        ev, data = d.get("event"), d.get("data")
        s = json.dumps(data)
        print(f"  EVENT {ev} {s[:300]}")
    c.on("*", _p)

    await c.connect()
    await c.enter_room(room_id)
    await asyncio.sleep(0.5)

    print("minting turnstile token...")
    async with TurnstileProvider() as tp:
        token = await tp.get_token()
    print("token:", token[:32], "...")

    try:
        await c.join_game("BenchBot-A", appearance="#5A99DA", captcha_token=token)
    except ActionError as e:
        print("join_game FAILED:", e.code, e)
        await c.close()
        return
    print("joined as:", json.dumps(c.self_player)[:240])

    # allow bots so the game can start with one human seat
    try:
        await c.update_game_room(canBotsJoin=True)
        print("canBotsJoin=True ok")
    except ActionError as e:
        print("update_game_room failed:", e.code, e)

    # wait for bots to fill in
    for i in range(30):
        parts = c.participants or {}
        players = [p for p in parts.values() if p]
        print(f"  waiting players={len(players)}")
        if len(players) >= 2:
            break
        await asyncio.sleep(1)

    try:
        await c.start_game()
        print("start_game ok")
    except ActionError as e:
        print("start_game failed:", e.code, e)

    # play: on our turn roll, maybe buy, end turn. crude loop.
    for i in range(40):
        await asyncio.sleep(1.2)
        if c.game_ended.is_set():
            break
        try:
            await c.roll_dice()
        except ActionError:
            pass
        await asyncio.sleep(0.8)
        for act in (c.buy_property, c.end_turn):
            try:
                await act()
            except ActionError:
                pass
            await asyncio.sleep(0.4)

    print("\n=== render ===")
    from richup.state import render
    print(render(c))
    await c.close()


if __name__ == "__main__":
    asyncio.run(main())
