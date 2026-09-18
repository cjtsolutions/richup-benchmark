"""MCP server exposing richup.io as agent tools.

One MCP server instance = one seat in one room. Tools:

  lobby/setup : create_room, join_room, list_lobby_rooms, update_settings, start_game
  observe     : get_state, get_board_text, poll_events
  turn        : roll_dice, end_turn, pay_out_of_prison, use_pardon_card
  property    : buy_property, sell_property, upgrade_city, downgrade_city,
                mortgage_property, lift_mortgage
  auction     : start_auction, auction_bid
  trade       : create_trade, confirm_trade, decline_trade, delete_trade
  social      : chat, bankrupt, request_clock_time, host_kick, votekick

Every mutating tool returns {ok, result|error, state} where `state` is the
fresh post-action summary — the agent never has to know the wire protocol.

Run:  python -m richup.mcp_server            (stdio)
"""

from __future__ import annotations

import logging
import sys
from typing import Any

from mcp.server.mcpserver import MCPServer

from . import state as st
from .client import ActionError
from .session import APPEARANCE_PALETTE, GameSession

log = logging.getLogger("richup.mcp")

server = MCPServer(
    "richup",
    instructions=(
        "Play richup.io (multiplayer Monopoly-style board game) through tools. "
        "Flow: create_room or join_room -> update_settings -> start_game -> "
        "get_state/poll_events each turn -> act with roll_dice/buy_property/"
        "end_turn/trade tools. get_state returns full board, money, ownership, "
        "turn info and available actions."
    ),
)

_session: GameSession | None = None


def _sess() -> GameSession:
    if _session is None:
        raise RuntimeError(
            "Not in a room yet — call create_room or join_room first."
        )
    return _session


async def _finish(result: Any = None) -> dict:
    """Attach a fresh post-action state summary to a tool result."""
    s = _sess()
    try:
        await s.client.sync()
    except Exception:
        pass
    return {
        "ok": True,
        "result": result,
        "state": st.summarize(s.client),
        "available_actions": st.available_actions(s.client),
    }


async def _act(fn, *args, **kwargs) -> dict:
    """Run a client action, normalize errors, return {ok,...}."""
    try:
        res = await fn(*args, **kwargs)
    except ActionError as e:
        return {"ok": False, "error": {"code": e.code, "message": str(e)}}
    except Exception as e:
        return {"ok": False, "error": {"code": type(e).__name__, "message": str(e)}}
    return await _finish(res)


# ====================================================================== setup
@server.tool(description=(
    "Create a new richup.io room and join it as a player. Launches the "
    "Turnstile bootstrap browser on first call (takes a few seconds); pass "
    "captcha_token to use a manually-solved token instead. Returns room_id."
))
async def create_room(
    name: str,
    appearance: str = "#5A99DA",
    is_private: bool = True,
    allow_bots: bool = True,
    captcha_token: str | None = None,
) -> dict:
    global _session
    if _session is not None:
        return {"ok": False, "error": {"code": "ALREADY_IN_ROOM",
                                       "message": "already seated; close this server or restart"}}
    _session = GameSession(name=name, appearance=appearance,
                           captcha_token=captcha_token)
    try:
        room_id = await _session.create_and_join(
            is_private=is_private,
            settings={"canBotsJoin": allow_bots} if allow_bots else None,
        )
    except Exception as e:
        _session = None
        return {"ok": False, "error": {"code": type(e).__name__, "message": str(e)}}
    return {
        "ok": True,
        "result": {
            "room_id": room_id,
            "url": f"https://richup.io/room/{room_id}",
            "player_id": _session.client.self_player_id,
            "palette": APPEARANCE_PALETTE,
        },
        "state": st.summarize(_session.client),
    }


@server.tool(description=(
    "Join an existing room by room id (e.g. 'x4sf7'). The id is in the room "
    "URL. Joins as a player via the Turnstile bootstrap. Pass captcha_token "
    "to use a manually-solved token instead of the automated browser mint."
))
async def join_room(room_id: str, name: str, appearance: str = "#5A99DA",
                    captcha_token: str | None = None) -> dict:
    global _session
    if _session is not None:
        return {"ok": False, "error": {"code": "ALREADY_IN_ROOM",
                                       "message": "already seated; close this server or restart"}}
    _session = GameSession(name=name, appearance=appearance,
                           captcha_token=captcha_token)
    try:
        await _session.join_existing(room_id)
    except Exception as e:
        _session = None
        return {"ok": False, "error": {"code": type(e).__name__, "message": str(e)}}
    return {
        "ok": True,
        "result": {"room_id": room_id,
                   "player_id": _session.client.self_player_id},
        "state": st.summarize(_session.client),
    }


@server.tool(description=(
    "The 'Play' button: matchmake into a public room of `max_players` size "
    "(2-4) and join as a player. This is how humans find public games — "
    "you'll share the table with real players, not just bots. The room "
    "host starts the game; use poll_events to watch for game-started."
))
async def quick_play(max_players: int = 4, name: str = "Agent",
                     appearance: str = "#5A99DA",
                     captcha_token: str | None = None) -> dict:
    global _session
    if _session is not None:
        return {"ok": False, "error": {"code": "ALREADY_IN_ROOM",
                                       "message": "already seated; close this server or restart"}}
    _session = GameSession(name=name, appearance=appearance,
                           captcha_token=captcha_token)
    try:
        room_id = await _session.quick_play(max_players)
    except Exception as e:
        _session = None
        return {"ok": False, "error": {"code": type(e).__name__, "message": str(e)}}
    return {
        "ok": True,
        "result": {"room_id": room_id,
                   "player_id": _session.client.self_player_id},
        "state": st.summarize(_session.client),
    }


@server.tool(description=(
    "Join a room by its share code (the short code in invites/room links, "
    "e.g. 'X4SF7'). Resolves the code then joins as a player."
))
async def join_room_by_code(code: str, name: str,
                            appearance: str = "#5A99DA",
                            captcha_token: str | None = None) -> dict:
    global _session
    if _session is not None:
        return {"ok": False, "error": {"code": "ALREADY_IN_ROOM",
                                       "message": "already seated; close this server or restart"}}
    _session = GameSession(name=name, appearance=appearance,
                           captcha_token=captcha_token)
    try:
        room_id = await _session.join_by_code(code)
    except Exception as e:
        _session = None
        return {"ok": False, "error": {"code": type(e).__name__, "message": str(e)}}
    return {
        "ok": True,
        "result": {"room_id": room_id,
                   "player_id": _session.client.self_player_id},
        "state": st.summarize(_session.client),
    }


@server.tool(description="List public rooms currently in the lobby.")
async def list_lobby_rooms() -> dict:
    if _session is not None:
        rooms = await _session.client.list_lobby_rooms()
    else:
        c = None
        try:
            from .client import RichUpClient
            c = RichUpClient()
            await c.init_session()
            rooms = await c.list_lobby_rooms()
        finally:
            if c is not None:
                await c.close()
    return {"ok": True, "result": rooms}


@server.tool(description=(
    "Update room settings (host only). Keys: canBotsJoin, isPrivate, "
    "maxPlayers (2-4+), startingCash (500-3000), auction, mortgage, "
    "evenBuild, vacationCash, payDoubleRentWhenOwnFullSet, "
    "noRentPaymentsWhileInPrison, shufflePlayerOrder, teams{enabled}."
))
async def update_settings(settings: dict) -> dict:
    return await _act(_sess().client.update_game_room, **(settings or {}))


@server.tool(description=(
    "Wait for seats to fill then start the game. If fill_bots, enables "
    "canBotsJoin first (server adds bots based on availability)."
))
async def start_game(fill_bots: bool = True, min_players: int = 2,
                     wait_seconds: int = 60) -> dict:
    s = _sess()
    try:
        await s.start(fill_bots=fill_bots, min_players=min_players,
                      wait_s=wait_seconds)
    except ActionError as e:
        return {"ok": False, "error": {"code": e.code, "message": str(e)}}
    except Exception as e:
        return {"ok": False, "error": {"code": type(e).__name__, "message": str(e)}}
    return await _finish({"started": True})


# =================================================================== observe
@server.tool(description=(
    "Force-sync and return the current game state: phase, whose turn, "
    "every player's money/position/properties, board blocks, auction, "
    "trades, and available_actions."
))
async def get_state() -> dict:
    s = _sess()
    await s.client.sync()
    return {
        "ok": True,
        "state": st.summarize(s.client),
        "available_actions": st.available_actions(s.client),
    }


@server.tool(description="Render the board as compact text (LLM-friendly).")
async def get_board_text() -> dict:
    return {"ok": True, "text": st.render(_sess().client)}


@server.tool(description=(
    "Return game events since `cursor` (default: last 25). Response includes "
    "the new cursor — pass it back next poll to get only new events. Events "
    "include dice-rolled, purchase-*, auction-*, trade-*, chat messages, "
    "player-bankrupted, game-ended, game-error."
))
async def poll_events(cursor: int = -25) -> dict:
    s = _sess()
    evs = list(s.client.events)
    n = len(evs)
    start = max(0, cursor) if cursor >= 0 else max(0, n + cursor)
    return {
        "ok": True,
        "cursor": n,
        "events": evs[start:],
    }


# ====================================================================== turn
@server.tool(description="Roll the dice (your turn, before moving).")
async def roll_dice() -> dict:
    return await _act(_sess().client.roll_dice)


@server.tool(description="End your turn (after rolling/resolving).")
async def end_turn() -> dict:
    return await _act(_sess().client.end_turn)


@server.tool(description="Pay to leave prison (when on the prison block).")
async def pay_out_of_prison() -> dict:
    return await _act(_sess().client.pay_out_of_prison)


@server.tool(description="Use a pardon/'get out of jail' card.")
async def use_pardon_card() -> dict:
    return await _act(_sess().client.use_pardon_card)


# ================================================================== property
@server.tool(description="Buy the unowned property you're standing on.")
async def buy_property() -> dict:
    return await _act(_sess().client.buy_property)


@server.tool(description="Sell your property at block_index back to the bank.")
async def sell_property(block_index: int) -> dict:
    return await _act(_sess().client.sell_property, block_index)


@server.tool(description="Add a house/hotel level on your city at block_index.")
async def upgrade_city(block_index: int) -> dict:
    return await _act(_sess().client.upgrade_city, block_index)


@server.tool(description="Remove a house/hotel level at block_index (refund).")
async def downgrade_city(block_index: int) -> dict:
    return await _act(_sess().client.downgrade_city, block_index)


@server.tool(description="Mortgage property at property_index (mortgage setting on).")
async def mortgage_property(property_index: int) -> dict:
    return await _act(_sess().client.mortgage_property, property_index)


@server.tool(description="Lift the mortgage at property_index.")
async def lift_mortgage(property_index: int) -> dict:
    return await _act(_sess().client.lift_mortgage, property_index)


# =================================================================== auction
@server.tool(description="Auction the unowned property you landed on (instead of buying).")
async def start_auction() -> dict:
    return await _act(_sess().client.start_auction)


@server.tool(description="Bid `amount` in the running auction.")
async def auction_bid(amount: int) -> dict:
    return await _act(_sess().client.auction_bid, amount)


# ===================================================================== trade
@server.tool(description=(
    "Create a trade offer. `trade` = {initiatorId, recipientId, "
    "initiatorOffer:{money, properties[], pardonCards?}, "
    "recipientOffer:{...}, note?}. Use get_state player ids/block indices."
))
async def create_trade(trade: dict, negotiated_trade_id: str | None = None) -> dict:
    return await _act(_sess().client.create_trade, trade, negotiated_trade_id)


@server.tool(description="Confirm/accept a pending trade by id.")
async def confirm_trade(trade_id: str) -> dict:
    return await _act(_sess().client.confirm_trade, trade_id)


@server.tool(description="Decline a pending trade by id.")
async def decline_trade(trade_id: str) -> dict:
    return await _act(_sess().client.decline_trade, trade_id)


@server.tool(description="Delete/cancel a trade you created.")
async def delete_trade(trade_id: str) -> dict:
    return await _act(_sess().client.delete_trade, trade_id)


# ==================================================================== social
@server.tool(description="Send a chat message to the room.")
async def chat(content: str) -> dict:
    return await _act(_sess().client.chat, content)


@server.tool(description="Declare bankruptcy (gives up; transfers assets per debtTo).")
async def bankrupt() -> dict:
    return await _act(_sess().client.bankrupt)


@server.tool(description="Ask other players to grant you more turn time.")
async def request_clock_time() -> dict:
    return await _act(_sess().client.request_clock_time)


@server.tool(description="Grant clock time to a player who requested it.")
async def grant_clock_time() -> dict:
    return await _act(_sess().client.grant_clock_time)


@server.tool(description="Vote to kick a player (id from get_state).")
async def votekick(player_id: str) -> dict:
    return await _act(_sess().client.votekick, player_id)


@server.tool(description="Kick a player as host.")
async def host_kick(player_id: str) -> dict:
    return await _act(_sess().client.host_kick, player_id)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stderr,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    import asyncio
    asyncio.run(server.run_stdio_async())


if __name__ == "__main__":
    main()
