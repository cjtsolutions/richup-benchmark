"""Async RichUp.io client — cookie session + socket.io + typed actions.

Mirrors the browser client's wire behavior:
  REST  (axios, baseURL /api, cookie session)      -> httpx.AsyncClient
  WS    (/api/game, /api/lobby namespaces)          -> python-socketio AsyncClient

Every client->server emit is acked; acks are {ok: bool, code?, message?, ...}.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from collections import deque
from collections.abc import Awaitable, Callable
from typing import Any, Self

import httpx
import socketio

from . import events as ev

log = logging.getLogger("richup.client")

DEFAULT_BASE_URL = "https://richup.io"
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)
ACK_TIMEOUT = 10.0
JOIN_TIMEOUT = 30.0

# events after which the game state is worth re-syncing from the server
_STATE_CHANGE_EVENTS = {
    ev.GAME_STARTED, ev.GAME_ENDED, ev.DICE_ROLLED, ev.TURN_ENDED,
    ev.PURCHASE_SUCCESS, ev.PROPERTY_SOLD, ev.CITY_LEVEL_CHANGED,
    ev.PROPERTY_MORTGAGED, ev.PROPERTY_MORTGAGE_LIFTED,
    ev.AUCTION_STARTED, ev.AUCTION_BADE, ev.AUCTION_ENDED,
    ev.TRADE_CREATED, ev.TRADE_CONFIRMED, ev.TRADE_DECLINED, ev.TRADE_DELETED,
    ev.PLAYER_BANKRUPTED, ev.PLAYER_VOTEKICKED, ev.PLAYER_HOST_KICKED,
    ev.CLOCK_TIME_GRANTED, ev.PAID_OUT_OF_PRISON, ev.USED_PARDON_CARD,
    ev.TEAM_UPDATED, ev.PLAYER_LEFT, ev.PLAYER_JOINED,
}


class ActionError(Exception):
    """Server returned {ok: false} (or a malformed ack) for an action emit."""

    def __init__(self, code: str, message: str, event: str | None = None):
        self.code = code
        self.event = event
        super().__init__(message if event is None else f"[{event}] {message}")


class ConnectionState:
    DISCONNECTED = "disconnected"
    CONNECTED = "connected"


EventHandler = Callable[[Any], Awaitable[None]]


class RichUpClient:
    """One seat at one room. Create a new instance per player/bot."""

    def __init__(self, base_url: str = DEFAULT_BASE_URL, *, verbose: bool = False):
        self.base_url = base_url.rstrip("/")
        self.http = httpx.AsyncClient(
            base_url=self.base_url,
            follow_redirects=True,
            headers={"User-Agent": USER_AGENT},
            timeout=30.0,
        )
        self.verbose = verbose

        # socket.io clients (separate engine.io connections, like the SPA)
        self.game_sio = socketio.AsyncClient(
            reconnection=True, reconnection_attempts=8,
            reconnection_delay=1, reconnection_delay_max=5,
            logger=verbose, engineio_logger=verbose,
        )
        self.lobby_sio = socketio.AsyncClient(
            reconnection=True, reconnection_attempts=8,
            reconnection_delay=1, reconnection_delay_max=5,
            logger=verbose, engineio_logger=verbose,
        )

        # --- tracked state ---------------------------------------------------
        self.connectivity = ConnectionState.DISCONNECTED
        self.room: dict | None = None              # last entered-room room obj
        self.self_participant_id: str | None = None  # socket-level participant id
        self.self_player_id: str | None = None       # player id inside the game
        self.is_player = False
        self.self_player: dict | None = None       # joined-game selfPlayer
        self.game_state: dict | None = None        # last sync-game-state gameState
        self.game_started = asyncio.Event()
        self.game_ended = asyncio.Event()
        self.game_end_payload: dict | None = None
        self.participants: dict[str, dict] = {}    # playerId -> participant

        self.events: deque[dict] = deque(maxlen=1000)   # raw event log
        self._handlers: dict[str, list[EventHandler]] = {}
        self._room_id: str | None = None
        self._in_room = asyncio.Event()
        self._connected = asyncio.Event()
        self._lobby_list_waiter: asyncio.Future | None = None
        self._sync_seq = 0                     # bumps on each sync-game-state
        self._sync_task: asyncio.Task | None = None
        self.auto_sync = True                  # debounced request-sync on changes
        self.server_time_offset = 0.0          # serverNow - localNow (ms)

        self._wire_game_socket()

    # ------------------------------------------------------------------ util
    def _cookie_header(self) -> str:
        return "; ".join(
            f"{c.name}={c.value}" for c in self.http.cookies.jar
        )

    async def __aenter__(self) -> Self:
        await self.init_session()
        return self

    async def __aexit__(self, *exc) -> None:
        await self.close()

    # ------------------------------------------------------------------ REST
    async def init_session(self) -> None:
        """Harvest the anonymous connect.sid cookie (401 is expected)."""
        try:
            await self.http.get("/api/auth/self")
        except httpx.HTTPError:
            pass
        if not self.http.cookies.jar:
            # fall back to any endpoint that sets the cookie
            try:
                await self.http.get("/api/features")
            except httpx.HTTPError:
                pass

    async def auth_self(self) -> dict | None:
        r = await self.http.get("/api/auth/self")
        return r.json() if r.status_code == 200 else None

    async def reauth(self) -> None:
        try:
            await self.http.post("/api/game/reauth")
        except httpx.HTTPError:
            pass

    async def create_room(self, is_private: bool = True) -> str:
        r = await self.http.get(f"/api/room/new?isPrivate={'true' if is_private else 'false'}")
        r.raise_for_status()
        data = r.json()
        return data.get("roomId") or data.get("id") or data

    async def find_room(self, code: str) -> str:
        r = await self.http.get(f"/api/room/find/{code}")
        r.raise_for_status()
        return r.json()["roomId"]

    async def lobby_landing(self, room_id: str = "") -> dict:
        r = await self.http.get(f"/api/lobby/landing?roomId={room_id}")
        r.raise_for_status()
        return r.json()

    async def get_maps(self) -> Any:
        r = await self.http.get("/api/game/maps")
        r.raise_for_status()
        return r.json()

    async def get_announcements(self) -> Any:
        r = await self.http.get("/api/announcements")
        r.raise_for_status()
        return r.json()

    async def keepalive(self) -> None:
        try:
            await self.http.get("/api/keepalive")
        except httpx.HTTPError:
            pass

    # -------------------------------------------------------------- sockets
    def _ws_headers(self) -> dict:
        return {
            "Cookie": self._cookie_header(),
            "Origin": self.base_url,
            "User-Agent": USER_AGENT,
        }

    def _wire_game_socket(self) -> None:
        sio = self.game_sio

        @sio.on("connect", namespace=ev.NS_GAME)
        async def _on_connect():
            self.connectivity = ConnectionState.CONNECTED
            self._connected.set()
            self._log_event("connect", {})
            # re-enter the room on reconnect, like the SPA does
            if self._room_id is not None:
                try:
                    await self.enter_room(self._room_id)
                except Exception as e:
                    log.warning("re-enter-room failed: %s", e)

        @sio.on("disconnect", namespace=ev.NS_GAME)
        async def _on_disconnect(reason=None):
            self.connectivity = ConnectionState.DISCONNECTED
            self._connected.clear()
            self._log_event("disconnect", {"reason": reason})

        @sio.on("*", namespace=ev.NS_GAME)
        async def _catch_all(event, *args):
            data = args[0] if len(args) == 1 else list(args)
            self._ingest(event, data)

    async def connect(self) -> None:
        """Open the /api/game socket (does not enter any room yet)."""
        if self.game_sio.connected:
            return
        await self.game_sio.connect(
            self.base_url,
            namespaces=[ev.NS_GAME],
            socketio_path=ev.SIO_PATH_GAME,
            transports=["websocket"],
            headers=self._ws_headers(),
            wait_timeout=15,
        )
        await asyncio.wait_for(self._connected.wait(), timeout=15)

    async def connect_lobby(self) -> None:
        """Open the /api/lobby namespace socket (rooms list)."""
        if self.lobby_sio.connected:
            return

        @self.lobby_sio.on(ev.LOBBY_ROOMS_LIST, namespace=ev.NS_LOBBY)
        async def _rooms(data):
            if self._lobby_list_waiter and not self._lobby_list_waiter.done():
                self._lobby_list_waiter.set_result(data)

        await self.lobby_sio.connect(
            self.base_url,
            namespaces=[ev.NS_LOBBY],
            socketio_path=ev.SIO_PATH_GAME,
            transports=["websocket"],
            headers=self._ws_headers(),
            wait_timeout=15,
        )

    async def list_lobby_rooms(self, timeout: float = 10) -> dict:
        """-> {rooms: [...], nextUpdate}"""
        await self.connect_lobby()
        loop = asyncio.get_running_loop()
        self._lobby_list_waiter = loop.create_future()
        await self.lobby_sio.emit(ev.GET_LOBBY_ROOMS_LIST, {}, namespace=ev.NS_LOBBY)
        return await asyncio.wait_for(self._lobby_list_waiter, timeout)

    async def close(self) -> None:
        if self._sync_task and not self._sync_task.done():
            self._sync_task.cancel()
        for sio in (self.game_sio, self.lobby_sio):
            try:
                if sio.connected:
                    await sio.disconnect()
            except Exception:
                pass
        await self.http.aclose()

    # ------------------------------------------------------------ subscribe
    def on(self, event: str, fn: EventHandler) -> None:
        """Register an extra handler for a /api/game event."""
        self._handlers.setdefault(event, []).append(fn)

    # -------------------------------------------------------------- internal
    def _log_event(self, event: str, data: Any) -> None:
        self.events.append({"t": time.time(), "event": event, "data": data})
        if self.verbose:
            log.info("<< %s %s", event, json.dumps(data)[:300])

    def _ingest(self, event: str, data: Any) -> None:
        """Update tracked state then dispatch to user handlers."""
        self._log_event(event, data)

        if event == ev.ENTERED_ROOM and isinstance(data, dict):
            self.room = data.get("room")
            self.self_participant_id = data.get("selfParticipantId")
            self.is_player = bool(data.get("isPlayer"))
            self._index_participants()
            self._in_room.set()
            if (self.room or {}).get("phase") == "playing":
                self.game_started.set()
        elif event == ev.JOINED_GAME and isinstance(data, dict):
            self.self_player = data.get("selfPlayer")
            self.is_player = True
            if self.self_player and self.self_player.get("id"):
                self.self_player_id = self.self_player["id"]
                self.participants[self.self_player_id] = self.self_player
        elif event == ev.PLAYER_JOINED and isinstance(data, dict):
            p = data.get("participant") or data
            pid = p.get("id") or p.get("participantId")
            if pid:
                self.participants[pid] = p
        elif event == ev.PLAYER_LEFT and isinstance(data, dict):
            self.participants.pop(data.get("playerId"), None)
        elif event == ev.GAME_STARTED:
            self.game_started.set()
            self.game_ended.clear()
            asyncio.ensure_future(self._calibrate_clock())  # noqa: RUF006
            if self.room is not None:
                self.room["phase"] = "playing"
            order = data.get("participantsOrder") if isinstance(data, dict) else None
            if order:
                for i, p in enumerate(order):
                    pid = p.get("id")
                    if pid:
                        p["orderIndex"] = i
                        self.participants[pid] = p
                        if self.self_player and pid == self.self_player.get("id"):
                            self.self_player = p
                            self.self_player_id = pid
        elif event == ev.SYNC_GAME_STATE and isinstance(data, dict):
            self.game_state = data.get("gameState", data)
            self._sync_seq += 1
            for p in self.game_state.get("participants") or []:
                if p.get("id"):
                    self.participants[p["id"]] = p
            if self.room is not None:
                self.room["phase"] = self.game_state.get("phase", self.room.get("phase"))
        elif event == ev.GAME_ENDED:
            self.game_end_payload = data if isinstance(data, dict) else {}
            self.game_ended.set()
            self.game_started.clear()
            if self.room is not None:
                self.room["phase"] = "ended"
        elif event in (ev.ROOM_DELETED, ev.ROOM_NOT_FOUND):
            self.room = None
            self.game_state = None
            self._in_room.clear()
        elif event == ev.GAME_ROOM_UPDATED and isinstance(data, dict):
            if self.room is not None:
                self._merge_room(data)

        for fn in self._handlers.get(event, []):
            asyncio.ensure_future(self._safe(fn, data))  # noqa: RUF006
        for fn in self._handlers.get("*", []):
            asyncio.ensure_future(  # noqa: RUF006
                self._safe(fn, {"event": event, "data": data})
            )

        if self.auto_sync and event in _STATE_CHANGE_EVENTS:
            self._schedule_sync()

    async def _calibrate_clock(self) -> None:
        try:
            await self.request_server_time()
        except Exception as e:
            log.debug("clock calibration failed: %s", e)

    # --------------------------------------------------------------- syncing
    def _schedule_sync(self) -> None:
        if self._sync_task is None or self._sync_task.done():
            self._sync_task = asyncio.ensure_future(self._auto_sync())

    async def _auto_sync(self) -> None:
        await asyncio.sleep(0.4)  # collapse bursts (e.g. a full turn)
        try:
            await self._act(ev.REQUEST_SYNC, {"snapshot": ""})
        except Exception as e:
            log.debug("auto-sync failed: %s", e)

    async def sync(self, timeout: float = 10.0) -> dict | None:
        """Force a state refresh; returns the fresh gameState dict."""
        before = self._sync_seq
        await self._act(ev.REQUEST_SYNC, {"snapshot": ""})
        deadline = asyncio.get_running_loop().time() + timeout
        while self._sync_seq == before:
            if asyncio.get_running_loop().time() > deadline:
                break
            await asyncio.sleep(0.05)
        return self.game_state

    async def _safe(self, fn: EventHandler, data: Any) -> None:
        try:
            await fn(data)
        except Exception as e:
            log.warning("handler error for %s: %s", fn, e)

    def _index_participants(self) -> None:
        if not self.room:
            return
        parts = (
            self.room.get("participants")
            or self.room.get("players")
            or []
        )
        if isinstance(parts, dict):
            parts = list(parts.values())
        for p in parts:
            pid = p.get("id") or p.get("participantId")
            if pid:
                self.participants[pid] = p

    def _merge_room(self, data: dict) -> None:
        # server sends a settings/room patch on game-room-updated
        if "settings" in data and self.room is not None:
            self.room.setdefault("settings", {}).update(data["settings"])
        for k, v in data.items():
            if k != "settings":
                self.room[k] = v
        self._index_participants()

    async def _act(self, event: str, data: Any = None, timeout: float = ACK_TIMEOUT) -> Any:
        """Emit an acked action; raise ActionError on {ok:false}."""
        await self.connect()
        try:
            ack = await self.game_sio.call(
                event, data if data is not None else {},
                namespace=ev.NS_GAME, timeout=timeout,
            )
        except socketio.exceptions.TimeoutError as err:
            raise ActionError(
                "ACK_TIMEOUT", f"no ack for {event!r} within {timeout}s", event
            ) from err
        # python-socketio returns the first ack arg (or tuple of args)
        payload = ack[0] if isinstance(ack, tuple) and ack else ack
        if isinstance(payload, dict):
            if payload.get("ok") is False:
                raise ActionError(
                    str(payload.get("code", "ERROR")),
                    str(payload.get("message", "action rejected")),
                    event,
                )
            return payload
        return {"ok": True, "raw": payload}

    # ============================================================== ACTIONS
    # ---- room ---------------------------------------------------------------
    async def enter_room(self, room_id: str) -> dict:
        self._room_id = room_id
        ack = await self._act(ev.ENTER_ROOM, {"roomId": room_id})
        # entered-room event usually arrives alongside/just after
        try:
            await asyncio.wait_for(self._in_room.wait(), timeout=5)
        except TimeoutError:
            pass
        return ack

    async def join_game(
        self,
        name: str,
        appearance: Any = None,
        bot: bool | None = None,
        captcha_token: str | None = None,
    ) -> dict:
        payload: dict[str, Any] = {"name": name}
        if appearance is not None:
            payload["appearance"] = appearance
        if bot is not None:
            payload["bot"] = bot
        if captcha_token is not None:
            payload["captchaToken"] = captcha_token
        return await self._act(ev.JOIN_GAME, payload, timeout=JOIN_TIMEOUT)

    async def update_game_room(self, **settings) -> dict:
        """Partial room settings update (host only)."""
        return await self._act(ev.UPDATE_GAME_ROOM, settings)

    async def update_appearance(self, appearance: Any) -> dict:
        return await self._act(ev.UPDATE_PLAYER_APPEARANCE, {"appearance": appearance})

    async def start_game(self) -> dict:
        return await self._act(ev.START_GAME)

    async def restart_room(self) -> dict:
        return await self._act(ev.ROOM_RESTART)

    async def votekick(self, player_id: str | None = None) -> dict:
        return await self._act(ev.VOTEKICK_PLAYER, {"playerId": player_id})

    async def host_kick(self, player_id: str) -> dict:
        return await self._act(ev.HOST_KICK_PLAYER, {"playerId": player_id})

    async def mute_player(self, player_id: str, muted: bool = True) -> dict:
        return await self._act(ev.MUTE_PLAYER, {"playerId": player_id, "muted": muted})

    async def report_player(self, player_id: str, reason: str) -> dict:
        return await self._act(ev.REPORT_PLAYER, {"playerId": player_id, "reason": reason})

    async def request_clock_time(self) -> dict:
        return await self._act(ev.REQUEST_CLOCK_TIME)

    async def grant_clock_time(self) -> dict:
        return await self._act(ev.GRANT_CLOCK_TIME)

    async def bankrupt(self) -> dict:
        return await self._act(ev.DO_BANKRUPT)

    async def team_action(self, payload: dict) -> dict:
        return await self._act(ev.TEAM_ACTION, payload)

    # ---- sync / turn / dice ---------------------------------------------------
    async def request_sync(self, snapshot: str = "") -> dict:
        return await self._act(ev.REQUEST_SYNC, {"snapshot": snapshot})

    async def request_server_time(self) -> dict:
        """Sync local clock with the server; stores the offset for clock math."""
        before = time.time() * 1000
        ack = await self._act(ev.REQUEST_SERVER_TIME)
        after = time.time() * 1000
        data = ack.get("data") if isinstance(ack, dict) else None
        st_ = (data or {}).get("serverTime") or (ack.get("serverTime") if isinstance(ack, dict) else None)
        if st_:
            # assume the server timestamp sits at the midpoint of our RTT
            self.server_time_offset = st_ - (before + after) / 2
        return ack

    def server_now_ms(self) -> float:
        """Best-estimate current server time (falls back to local)."""
        return time.time() * 1000 + (self.server_time_offset or 0.0)

    async def roll_dice(self) -> dict:
        return await self._act(ev.PLZ_ROLL_DICES)

    async def end_turn(self) -> dict:
        return await self._act(ev.END_TURN)

    async def pay_out_of_prison(self) -> dict:
        return await self._act(ev.PAY_OUT_OF_PRISON)

    async def use_pardon_card(self) -> dict:
        return await self._act(ev.USE_PARDON_CARD)

    # ---- property / auction ---------------------------------------------------
    async def buy_property(self) -> dict:
        return await self._act(ev.PURCHASE_PROPERTY)

    async def sell_property(self, block_index: int) -> dict:
        return await self._act(ev.SELL_PROPERTY, {"blockIndex": block_index})

    async def upgrade_city(self, block_index: int) -> dict:
        return await self._act(ev.UPGRADE_CITY, {"blockIndex": block_index})

    async def downgrade_city(self, block_index: int) -> dict:
        return await self._act(ev.DOWNGRADE_CITY, {"blockIndex": block_index})

    async def start_auction(self) -> dict:
        return await self._act(ev.START_AUCTION)

    async def auction_bid(self, amount: int) -> dict:
        return await self._act(ev.AUCTION_BID, {"amount": amount})

    async def mortgage_property(self, property_index: int) -> dict:
        return await self._act(ev.MORTGAGE_PROPERTY, {"propertyIndex": property_index})

    async def lift_mortgage(self, property_index: int) -> dict:
        return await self._act(ev.LIFT_PROPERTY_MORTGAGE, {"propertyIndex": property_index})

    # ---- trading ----------------------------------------------------------------
    async def create_trade(self, trade: dict, negotiated_trade_id: str | None = None) -> dict:
        return await self._act(ev.CREATE_TRADE, {
            "trade": trade, "negotiatedTradeId": negotiated_trade_id,
        })

    async def confirm_trade(self, trade_id: str) -> dict:
        return await self._act(ev.CONFIRM_TRADE, {"tradeId": trade_id})

    async def decline_trade(self, trade_id: str) -> dict:
        return await self._act(ev.DECLINE_TRADE, {"tradeId": trade_id})

    async def delete_trade(self, trade_id: str) -> dict:
        return await self._act(ev.DELETE_TRADE, {"tradeId": trade_id})

    async def set_trade_watch(self, trade_id: str, is_watching: bool) -> dict:
        return await self._act(ev.SET_TRADE_WATCH_STATE,
                               {"tradeId": trade_id, "isWatching": is_watching})

    async def set_trade_creator(self, is_creating: bool) -> dict:
        return await self._act(ev.SET_TRADE_CREATOR_STATE, {"isCreating": is_creating})

    # ---- chat / admin -----------------------------------------------------------
    async def chat(self, content: str) -> dict:
        return await self._act(ev.CHAT_SEND_MESSAGE, content)

    async def chat_team(self, content: str) -> dict:
        return await self._act(ev.CHAT_SEND_TEAM_MESSAGE, content)

    async def chat_admin(self, content: str) -> dict:
        return await self._act(ev.CHAT_SEND_ADMIN_MESSAGE, content)

    async def chat_typing(self) -> dict:
        return await self._act(ev.CHAT_TYPING)

    async def admin_kick(self, participant_id: str, reason: str) -> dict:
        return await self._act(ev.ADMIN_KICK_PARTICIPANT,
                               {"participantId": participant_id, "reason": reason})
