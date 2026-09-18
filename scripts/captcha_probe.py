"""Probe join-game variants to see when captchaToken is required."""

import asyncio
import json
import sys

sys.path.insert(0, ".")
from richup.client import ActionError, RichUpClient


async def try_join(c, label, **kw):
    try:
        ack = await c.join_game(**kw)
        print(f"[{label}] OK -> {json.dumps(ack)[:200]}")
        return True
    except ActionError as e:
        print(f"[{label}] FAIL code={e.code} msg={e}")
        return False


async def main():
    c = RichUpClient()
    await c.init_session()
    room_id = await c.create_room(is_private=True)
    print("room:", room_id)
    await c.connect()
    await c.enter_room(room_id)

    await try_join(c, "bot=true", name="B1", bot=True)
    await try_join(c, "appearance=str", name="P1", appearance="blue")
    await try_join(c, "appearance=obj", name="P2", appearance={"color": "blue"})
    await try_join(c, "captcha=''", name="P3", captcha_token="")

    await asyncio.sleep(0.5)
    print("participants:", list(c.participants))
    print("is_player:", c.is_player, "self:", c.self_player)
    await c.close()


if __name__ == "__main__":
    asyncio.run(main())
