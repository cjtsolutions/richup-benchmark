"""Game-state extraction and text rendering for agents.

The authoritative state is the `sync-game-state` `gameState` object
(schema verified against live traffic):

    {
      id, phase ("lobby"|"playing"|"ended"), participants[], currentPlayerIndex,
      mapId, blocks[], boardConfig{goReward,prisonBlockIndex,goToPrisonBlockIndex,
      vacationBlockIndex}, dice[2], cubesRolledInTurn, canPerformTurnActions,
      doublesInARow, forceNoAnotherTurn, teams[], votekickerIds[], turnClock{...},
      auction|null, trades[], tradeCreatorIds[], bonusCards{...}, vacationCash,
      settings{...}, stampedFlags, hostId, winnerId, stats{...}
    }

participants[] entries: {id,name,appearance,isBot,teamId,position,money,
bankruptedAt,debtTo,connectivity,...,clock{bankMs,autoActedTurns,turnsTaken}}

blocks[] entries: {name,type("corner"|"city"|"airport"|"company"|"bonus"),
price?,ownerId?,isMortgaged?,countryId?,rentPrices?,level?,housePrice?,
hotelPrice?,bonusType?,cornerType?}
"""

from __future__ import annotations

from typing import Any

OWNED_TYPES = {"city", "airport", "company"}


def gs_of(client) -> dict | None:
    return client.game_state


def player_list(gs: dict | None) -> list[dict]:
    if not gs:
        return []
    return [p for p in gs.get("participants") or [] if isinstance(p, dict)]


def blocks(gs: dict | None) -> list[dict]:
    if not gs:
        return []
    return [b for b in gs.get("blocks") or [] if isinstance(b, dict)]


def block_at(gs: dict | None, index: int | None) -> dict | None:
    bs = blocks(gs)
    if index is None or not (0 <= index < len(bs)):
        return None
    return bs[index]


def current_player(gs: dict | None) -> dict | None:
    ps = player_list(gs)
    cpi = (gs or {}).get("currentPlayerIndex")
    if cpi is None or not (0 <= cpi < len(ps)):
        return None
    return ps[cpi]


def find_player(gs: dict | None, pid: str | None) -> dict | None:
    for p in player_list(gs):
        if p.get("id") == pid:
            return p
    return None


def me(client) -> dict | None:
    gs = client.game_state
    pid = client.self_player_id
    if gs:
        m = find_player(gs, pid)
        if m:
            return m
    return client.self_player


def owned_blocks(gs: dict | None, pid: str | None) -> list[tuple[int, dict]]:
    return [(i, b) for i, b in enumerate(blocks(gs)) if b.get("ownerId") == pid]


def suspended_turns(gs: dict | None, pid: str | None,
                    corner: str = "prison") -> int:
    """Turns a player is suspended at the prison/vacation corner block.

    The corner block carries `suspendedTurnsRemaining: {playerId: n}` —
    standing *on* the block is just visiting; only this map marks real
    imprisonment/vacation.
    """
    if not gs or pid is None:
        return 0
    cfg = gs.get("boardConfig") or {}
    idx = cfg.get("prisonBlockIndex" if corner == "prison"
                  else "vacationBlockIndex")
    b = block_at(gs, idx) or {}
    return int((b.get("suspendedTurnsRemaining") or {}).get(pid) or 0)


def in_prison(gs: dict | None, pid: str | None) -> bool:
    return suspended_turns(gs, pid, "prison") > 0


def clock_info(client, gs: dict | None = None) -> dict:
    """Turn-clock snapshot. The server gives each turn:

      graceMs (20s) -> the current player's bankMs drains -> expiry.

    Expiry => server auto-acts and autoActedTurns++; 2 strikes => removed.
    `turnExpiresInMs` is the hard deadline for the current turn (whoever's
    it is); `graceEndsInMs` is when the free window ends for the current
    player. Debted players get debtGraceMs instead of graceMs.
    """
    gs = gs if gs is not None else client.game_state
    gs = gs or {}
    tc = gs.get("turnClock") or {}
    cfg = tc.get("config") or {}
    turn = tc.get("turn") or {}
    cur = current_player(gs) or {}
    now = client.server_now_ms()
    started = turn.get("turnStartedAt") or now
    grace = cfg.get("debtGraceMs") if turn.get("debtGraceLatched") \
        else cfg.get("graceMs", 20000)
    grace = grace if grace is not None else 20000
    reserve_starts = started + turn.get("pausedMs", 0) \
        + turn.get("offlineMs", 0) + grace
    cur_bank = ((cur.get("clock") or {}).get("bankMs")) or 0
    expires = reserve_starts + turn.get("grantedMs", 0) + cur_bank
    me_p = find_player(gs, client.self_player_id) or {}
    my_clock = me_p.get("clock") or {}
    return {
        "turnExpiresInMs": int(expires - now),
        "graceEndsInMs": int(reserve_starts - now),
        "currentPlayerBankMs": cur_bank,
        "myBankMs": my_clock.get("bankMs"),
        "myAutoActedTurns": my_clock.get("autoActedTurns", 0),
        "removalAfterAutoActedTurns": cfg.get("removalAfterAutoActedTurns"),
        "autoActing": turn.get("autoActing", False),
    }


def block_label(i: int, b: dict, players_by_id: dict[str, dict] | None = None) -> str:
    name = b.get("name", f"#{i}")
    owner = b.get("ownerId")
    tag = ""
    if owner:
        pname = (players_by_id or {}).get(owner, {}).get("name", owner[:6])
        tag = f"@{pname}"
        lvl = b.get("level")
        if lvl:
            tag += f"+{lvl}"
        if b.get("isMortgaged"):
            tag += "(mortgaged)"
    return f"{i}:{name}{tag}"


def summarize(client) -> dict:
    """Structured snapshot for an agent (JSON-safe)."""
    gs = client.game_state or {}
    pid = client.self_player_id
    cur = current_player(gs)
    players = []
    pb = {p.get("id"): p for p in player_list(gs)}
    for p in player_list(gs):
        owned = owned_blocks(gs, p.get("id"))
        players.append({
            "id": p.get("id"),
            "name": p.get("name"),
            "isBot": p.get("isBot"),
            "money": p.get("money"),
            "position": p.get("position"),
            "positionName": (block_at(gs, p.get("position")) or {}).get("name"),
            "bankrupted": p.get("bankruptedAt") is not None,
            "debtTo": p.get("debtTo"),
            "inPrison": in_prison(gs, p.get("id")),
            "suspendedTurns": suspended_turns(gs, p.get("id")),
            "connectivity": p.get("connectivity"),
            "properties": [
                {"index": i, "name": b.get("name"), "type": b.get("type"),
                 "level": b.get("level"), "mortgaged": b.get("isMortgaged")}
                for i, b in owned
            ],
        })
    me_ = me(client) or {}
    phase = gs.get("phase") or (client.room or {}).get("phase")
    playing = phase == "playing"
    return {
        "phase": phase,
        "roomId": (client.room or {}).get("id") or client._room_id,
        "hostId": gs.get("hostId"),
        "turn": {
            "currentPlayerId": (cur or {}).get("id") if playing else None,
            "currentPlayerName": (cur or {}).get("name") if playing else None,
            "isMyTurn": bool(playing and cur and cur.get("id") == pid),
            "canPerformTurnActions": gs.get("canPerformTurnActions") if playing else None,
            "cubesRolledInTurn": gs.get("cubesRolledInTurn") if playing else None,
            "dice": gs.get("dice") if playing else None,
            "doublesInARow": gs.get("doublesInARow") if playing else None,
            "forceNoAnotherTurn": gs.get("forceNoAnotherTurn") if playing else None,
        },
        "clock": clock_info(client, gs) if playing else None,
        "self": {
            "playerId": pid,
            "name": me_.get("name"),
            "money": me_.get("money"),
            "position": me_.get("position"),
            "positionName": (block_at(gs, me_.get("position")) or {}).get("name"),
            "debtTo": me_.get("debtTo"),
            "bankrupted": me_.get("bankruptedAt") is not None,
            "inPrison": in_prison(gs, pid),
        },
        "players": players,
        "blocks": [
            {"index": i, "name": b.get("name"), "type": b.get("type"),
             "price": b.get("price"), "ownerId": b.get("ownerId"),
             "level": b.get("level"), "mortgaged": b.get("isMortgaged"),
             "countryId": b.get("countryId"), "rentPrices": b.get("rentPrices"),
             "housePrice": b.get("housePrice")}
            for i, b in enumerate(blocks(gs))
        ],
        "auction": gs.get("auction"),
        "trades": gs.get("trades") or [],
        "vacationCash": gs.get("vacationCash"),
        "settings": gs.get("settings") or (client.room or {}).get("settings"),
        "boardConfig": gs.get("boardConfig"),
        "winnerId": gs.get("winnerId"),
    }


def available_actions(client) -> list[str]:
    """Best-effort list of actions the agent can take right now."""
    gs = client.game_state
    room = client.room or {}
    phase = (gs or {}).get("phase") or room.get("phase")
    acts: list[str] = []
    if client.room is None:
        return acts
    if phase in (None, "lobby", "waiting"):
        acts += ["update_game_room"]
        if not client.is_player:
            acts.append("join_game")
        if client.is_player:
            acts.append("start_game")
        return acts
    if not gs or phase == "ended":
        return acts
    s = summarize(client)
    turn = s["turn"]
    me_ = me(client) or {}
    pos = me_.get("position")
    blk = block_at(gs, pos) or {}
    imprisoned = in_prison(gs, client.self_player_id)

    if turn["isMyTurn"]:
        if imprisoned:
            acts += ["pay_out_of_prison", "use_pardon_card"]
        acts.append("request_clock_time")
        if not turn["cubesRolledInTurn"]:
            acts.append("roll_dice")
        else:
            if blk.get("type") in OWNED_TYPES and blk.get("ownerId") is None \
                    and blk.get("price") is not None:
                acts.append("buy_property")
                if (gs.get("settings") or {}).get("auction"):
                    acts.append("start_auction")
            acts.append("end_turn")
    if s["auction"]:
        acts += ["auction_bid"]
    # trades/property management generally available to players
    if client.is_player and not me_.get("bankruptedAt"):
        acts += ["create_trade", "chat"]
        owned = [b for b in gs.get("blocks") or []
                 if b.get("ownerId") == client.self_player_id]
        if owned:
            acts.append("sell_property")
            if any(b.get("type") == "city" for b in owned):
                acts += ["upgrade_city"]
            if any(b.get("type") == "city" and (b.get("level") or 0) > 0
                   for b in owned):
                acts.append("downgrade_city")
            if (gs.get("settings") or {}).get("mortgage"):
                if any(not b.get("isMortgaged") for b in owned):
                    acts.append("mortgage_property")
                if any(b.get("isMortgaged") for b in owned):
                    acts.append("lift_mortgage")
    return acts


def render(client, *, recent_events: int = 10, show_board: bool = True) -> str:
    """Compact text board for an LLM prompt."""
    out: list[str] = []
    gs = client.game_state
    s = summarize(client)
    room_id = s["roomId"] or "?"
    out.append(f"room={room_id} phase={s['phase']}")

    if s["phase"] in (None, "lobby", "waiting") and not gs:
        st = s.get("settings") or {}
        if st:
            keys = ("maxPlayers", "canBotsJoin", "isPrivate", "startingCash",
                    "auction", "mortgage", "evenBuild", "vacationCash")
            out.append("settings: " + ", ".join(
                f"{k}={st[k]}" for k in keys if k in st))
        parts = list(client.participants.values())
        if client.self_player:
            parts = [client.self_player] + [p for p in parts
                                            if p.get("id") != client.self_player_id]
        out.append("players in lobby: " + (", ".join(
            f"{p.get('name','?')}({'bot' if p.get('isBot') else 'human'})"
            for p in parts) or "none"))
    else:
        t = s["turn"]
        out.append(
            f"turn: current={t['currentPlayerName']} "
            f"myTurn={t['isMyTurn']} canAct={t['canPerformTurnActions']} "
            f"dice={t['dice']} rolled={t['cubesRolledInTurn']} "
            f"doubles={t['doublesInARow']}"
        )
        clk = s.get("clock") or {}
        if clk:
            left = max(0, (clk["turnExpiresInMs"] or 0) / 1000)
            urgent = left < 12
            strikes = clk.get("myAutoActedTurns")
            limit = clk.get("removalAfterAutoActedTurns")
            out.append(
                f"clock: turn expires in {left:.0f}s "
                f"(grace ends in {max(0, (clk['graceEndsInMs'] or 0) / 1000):.0f}s,"
                f" my bank {(clk['myBankMs'] or 0) / 1000:.0f}s)"
                + (f" | strikes {strikes}/{limit} — next timeout removes you!"
                   if strikes else "")
                + (" | URGENT: act now" if urgent else ""))
        me_ = s["self"]
        out.append(
            f"me: {me_['name']} ${me_['money']} pos={me_['position']}"
            f"({me_['positionName']})"
            + (f" debtTo={me_['debtTo']}" if me_.get("debtTo") else "")
        )
        for p in s["players"]:
            line = f"  {p['name']} ${p['money']} pos={p['position']}({p['positionName']})"
            owned = p["properties"]
            if owned:
                line += " props=[" + ", ".join(
                    f"{pr['index']}:{pr['name']}"
                    + (f"+{pr['level']}" if pr.get("level") else "")
                    + ("(M)" if pr.get("mortgaged") else "")
                    for pr in owned) + "]"
            flags = []
            if p.get("isBot"):
                flags.append("bot")
            if p.get("bankrupted"):
                flags.append("BANKRUPT")
            if p.get("inPrison"):
                flags.append(f"prison({p['suspendedTurns']})")
            if p.get("connectivity") not in (None, "stable", "connected"):
                flags.append(p["connectivity"])
            if flags:
                line += f" [{','.join(flags)}]"
            if p["id"] == t["currentPlayerId"]:
                line += " <- turn"
            if p["id"] == client.self_player_id:
                line += " (me)"
            out.append(line)
        if s["auction"]:
            out.append(f"auction: {s['auction']}")
        for tr in s["trades"]:
            out.append(f"trade: {tr}")
        if s.get("vacationCash"):
            out.append(f"vacationCash={s['vacationCash']}")
        if show_board and gs:
            pb = {p.get("id"): p for p in player_list(gs)}
            track = " | ".join(
                block_label(i, b, pb) for i, b in enumerate(blocks(gs))
            )
            out.append("board: " + track)

    evs = [e for e in client.events if e["event"] not in ("connect",)][-recent_events:]
    if evs:
        out.append("recent events:")
        for e in evs:
            out.append(f"  {e['event']}: {str(e['data'])[:160]}")
    out.append("actions: " + ", ".join(available_actions(client)))
    return "\n".join(out)
