# RichUp.io Protocol — Reverse-Engineered

Recovered from the production frontend bundles (`index.*.js`, `GamePageContent.*.js`,
`confetti.module.*.js`, `luxon.*.js`, `Lobby.*.js`) on 2026-09-18.

## Transport

- **Engine.IO v4 / Socket.IO v4**, WebSocket-only transport (`transports:["websocket"]`).
- No binary payloads; all messages are JSON (`42["event",{...}]`).
- Every client→server **action** emit expects an **ack**: `{ok: true, ...}` or
  `{ok: false, code, message}` (client throws `MALFORMED_ACK` when `ok` is absent).
  Default ack timeout 10 s (`join-game` uses 30 s).
- Engine.IO path is **per-namespace**:

| Namespace   | Engine.IO path             | Purpose                        |
|-------------|----------------------------|--------------------------------|
| `/api/app`  | `/api/app/socket.io/`      | social: friends, coin rewards  |
| `/api/game` | `/api/game/socket.io/`     | rooms + gameplay (main socket) |
| `/api/lobby`| `/api/game/socket.io/`     | lobby room list                |

Handshake (verified live):
`GET https://richup.io/api/game/socket.io/?EIO=4&transport=polling`
→ `0{"sid":"…","upgrades":["websocket"],"pingInterval":25000,"pingTimeout":20000}`

## Auth

- Cookie session `connect.sid` (express-session style), `HttpOnly; Secure; SameSite=Lax`.
- Issued automatically by any `/api/*` request — `GET /api/auth/self` returns **401**
  for anonymous users **but still sets the cookie**.
- Registered users use OAuth popup flows; **guests need nothing but the cookie**.
- `POST /api/game/reauth` — best-effort session refresh before joining (optional).
- Cloudflare Turnstile `captchaToken` is **required for every player join**
  (verified live: `join-game` without it is rejected). Sitekey:
  `0x4AAAAAAC08XOgqbge2s3TZ`. The SPA mints it via an invisible
  `turnstile.execute()` widget gated behind a `captcha` feature flag; it also
  suspends the whole room route until the token resolves ("Loading game...").

## REST (axios `baseURL:"/api"`, `withCredentials`)

| Method | Path | Notes |
|--------|------|-------|
| GET  | `/auth/self` | user or 401 (sets `connect.sid`) |
| GET  | `/room/new?isPrivate={bool}` | → `{roomId}` create room |
| GET  | `/room/find/{code}` | → `{roomId}` resolve share code **or matchmake**: `/room/find/{2,3,4}` returns a public room of that size (this is the "Play" button; non-numeric strings = share codes) |
| GET  | `/lobby/landing?roomId=` | landing data |
| GET  | `/game/maps` | available board maps |
| GET  | `/game/invite?params` | invite data |
| GET  | `/features` | feature flags |
| GET  | `/announcements` | lobby announcements |
| GET  | `/keepalive` | session keepalive |
| GET  | `/maintenance/maintenance-info` | |
| POST | `/game/reauth` | refresh session |
| POST | `/game/claim-coin-reward` | post-win coins |
| GET  | `/user/{id}/profile` · `/user/{id}/last-games?page=` | |
| POST | `/user/bulk` `{userIds:[]}` | batch user lookup |
| POST | `/user/self/update-name` `{name}` | |
| GET/POST | `/push/*`, `/user/friends`, `/user/{id}/friendship`, `/user/{id}/block` | social |

## `/api/lobby` namespace

| Dir | Event | Payload |
|-----|-------|---------|
| emit | `get-lobby-rooms-list` | `{}` |
| on   | `lobby-rooms-list` | `{rooms:[...]|"same", nextUpdate}` — `"same"` = no change since last poll |

## `/api/app` namespace (social — not needed for gameplay)

on: `newCoinReward {reason,amount}`, `friendshipStateChanged {friend,state}`,
`friendRoomInvite {friend,roomId}`

## `/api/game` namespace — room lifecycle

Client→server (all acked):

| Method | Event | Args |
|--------|-------|------|
| enterRoom | `enter-room` | `{roomId}` |
| joinGame | `join-game` | `{name, appearance, captchaToken, bot?}` — appearance required (palette hex), captchaToken required |
| updateGameRoom | `update-game-room` | partial settings, e.g. `{mapId}` |
| updatePlayerAppearance | `update-player-appearance` | `{appearance}` |
| startGame | `start-game` | — |
| restartRoom | `room-restart` | — |
| votekickPlayer | `votekick-player` | `{playerId}` (null = vote yes?) |
| hostKickPlayer | `host-kick-player` | `{playerId}` |
| mutePlayer | `mute-player` | `{playerId, muted}` |
| reportPlayer | `report-player` | `{playerId, reason}` |
| grantClockTime | `grant-clock-time` | — |
| requestClockTime | `request-clock-time` | — |
| submitBankrupt | `do-bankrupt` | — |
| teamAction | `team-action` | `{...}` |

Server→client:

| Event | Payload |
|-------|---------|
| `entered-room` | `{room, selfParticipantId, isPlayer, mutedPlayerIds, reportedPlayerIds, lostSeat}` — `room` has `settings`, `participants`, `phase`, `turnClock{config,turn}`, `stampedFlags` |
| `joined-game` | `{selfPlayer}` |
| `player-joined` | participant object |
| `player-left` | `{playerId}` |
| `game-error` | error object (bypassQueue) |
| `game-ended` | `{winnerId, coinRewardSeatId?}` |
| `room-deleted` | — |
| `room-not-found` | — |
| `game-room-updated` | settings/room patch |
| `player-votekicked` | `{playerId, votingPlayerId, forced, snapshot}` |
| `new-votekick-request` | `{votingPlayerId, snapshot}` |
| `player-host-kicked` | `{playerId, snapshot}` |
| `player-bankrupted` | `{playerId}` |
| `player-appearance-updated` | `{playerId, appearance}` |
| `participant-account-linked` | `{participantId, userId, name}` |
| `participant-connectivity-changed` | `{participantId, connectivity, connectivityKickAt?, offlineSince?}` |
| `clock-time-requested` | `{playerId}` |
| `clock-time-granted` | `{granterId, snapshot}` |
| `team-updated` | team object |

### Room settings (defaults)

```json
{ "maxPlayers": 4, "canBotsJoin": true, "isPrivate": false, "onlyUsers": false,
  "payDoubleRentWhenOwnFullSet": false, "vacationCash": false, "auction": false,
  "noRentPaymentsWhileInPrison": false, "mortgage": false, "startingCash": 1500,
  "evenBuild": true, "shufflePlayerOrder": true, "teams": {"enabled": false} }
```
`startingCash ∈ {500,1000,1500,2000,2500,3000}`. `update-game-room` takes a partial.
`canBotsJoin:true` → **server auto-fills seats with bots** ("based on
availability") — no client action needed (verified live: 3 bots joined a
fresh private room within ~5 s).

`join-game` `appearance` = a hex color string from the guest palette:

```json
["#C0DA5A","#FFC73F","#FF843F","#C34848","#5A99DA","#7FE7F5",
 "#009688","#73E85D","#9A6E5E","#C63FA2","#FF7CA0","#7F5ADA"]
```

`join-game` `bot` is **not** a boolean you can set — it must be a
server-issued signed token; forged values are rejected. To play vs bots,
create a room + `canBotsJoin` instead.

## `/api/game` — gameplay (turn / dice)

| Dir | Event | Args / Payload |
|-----|-------|----------------|
| emit | `request-sync` | `{snapshot}` (client state hash; server resyncs if stale) |
| on   | `sync-game-state` | `{gameState, ...}` full authoritative snapshot (bypassQueue, resets incoming queue) |
| emit | `start-game` | — |
| on   | `game-started` | `{participantsOrder:[{id}...]}` |
| emit | `plz-roll-dices` | — (yes, "plz-roll-dices") |
| on   | `dice-rolled` | `{dice:[d1,d2], snapshot, auto}` |
| emit | `end-turn` | — |
| on   | `turn-ended` | `{auto?}` |
| emit | `pay-out-of-prison` | — |
| on   | `paid-out-of-prison` | — |
| emit | `use-pardon-card` | — |
| on   | `used-pardon-card` | — |
| emit | `request-server-time` | — |

## `/api/game` — property / auction

| Dir | Event | Args / Payload |
|-----|-------|----------------|
| emit | `purchase-property` | — |
| on   | `purchase-success` | `{blockIndex}` |
| on   | `purchase-failed` | — |
| emit | `sell-property` | `{blockIndex}` |
| on   | `property-sold` | `{blockIndex}` |
| emit | `upgrade-city` | `{blockIndex}` (build house/hotel) |
| emit | `downgrade-city` | `{blockIndex}` |
| on   | `city-level-changed` | `{blockIndex, changeType}` |
| emit | `start-auction` | — |
| on   | `auction-started` | `{blockIndex, auto}` |
| emit | `auction-bid` | `{amount}` |
| on   | `auction-bade` | `{amount, bidderId, endsAt}` |
| on   | `auction-ended` | `{blockIndex, price, buyerId}` |
| emit | `mortgage-property` | `{propertyIndex}` |
| on   | `property-mortgaged` | `{propertyIndex}` |
| emit | `lift-property-mortgage` | `{propertyIndex}` |
| on   | `property-mortgage-lifted` | `{propertyIndex}` |

## `/api/game` — trading

| Dir | Event | Args / Payload |
|-----|-------|----------------|
| emit | `create-trade` | `{trade, negotiatedTradeId?}` |
| on   | `trade-created` | `{trade, negotiatedTradeId?}` |
| emit | `confirm-trade` | `{tradeId}` |
| on   | `trade-confirmed` | `{tradeId}` |
| emit | `decline-trade` | `{tradeId}` |
| on   | `trade-declined` | `{tradeId}` |
| emit | `delete-trade` | `{tradeId}` |
| on   | `trade-deleted` | `{tradeId, auto?}` |
| emit | `set-trade-watch-state` | `{tradeId, isWatching}` |
| on   | `trade-watch-state-changed` | `{tradeId, watcherId, isWatching}` |
| emit | `set-trade-creator-state` | `{isCreating}` |
| on   | `trade-creator-changed` | `{playerId, isCreating}` |

Trade object (from `propose-trade` server action): `{id, initiatorId, recipientId,
initiatorOffer, recipientOffer, note}`. Offers contain money / property block
indexes / pardon cards.

## `/api/game` — chat / admin

| Dir | Event | Args / Payload |
|-----|-------|----------------|
| emit | `chat:send-message` | raw message string (SPA verified: `sendMessage(t)` → `rr(e,oY,t)`, not wrapped in `{content}`) |
| on   | `chat:message-received` | `{senderId, content}` |
| emit | `chat:typing` | — |
| on   | `chat:participant-typing` | `{participantId}` |
| emit | `chat:send-team-message` | raw message string |
| on   | `chat:team-message-received` | `{senderId, content}` |
| emit | `chat:send-admin-message` | raw message string |
| on   | `chat:admin-message-received` | `{content}` |
| emit | `admin:kick-participant` | `{participantId, reason}` |
| on   | `admin:kicked-participant` | `{participantId}` |

## Client-side "server actions" (state machine, not wire events)

The client mirrors server state with `applyServerAction({type:...})`. Useful
vocabulary for interpreting snapshots:
`propose-trade`, `accept-trade`, `reject-trade`, `cancel-trade`,
`set-trade-watch-state`, `set-trade-creator-state`, `send-chat-message`,
`end-auction`, `unmortgage-property`, `update-player-connectivity`, …

## Connection flow (as the SPA does it)

1. `GET /api/auth/self` → harvest `connect.sid` (401 is fine).
2. Optional `POST /api/game/reauth`.
3. Open WS → engine.io `0{...}` → socket.io `40/api/game,` → `40{"sid":...}`.
4. On socket `connect`: emit `enter-room {roomId}` → `entered-room` (full room state).
5. Mint a Turnstile token (invisible widget on richup.io), then emit
   `join-game {name, appearance, captchaToken}` → `joined-game {selfPlayer}`.
   (Spectators skip this. Server validates the token server-side.)
6. Host emits `start-game` → `game-started {participantsOrder}` → `sync-game-state`.
7. Play: on your turn `plz-roll-dices` → `dice-rolled` → optional
   `purchase-property`/`start-auction`/`upgrade-city`/`trade`… → `end-turn`.
8. `request-sync {snapshot}` any time to force a resync; server pushes
   `sync-game-state` when state drifts.

## `gameState` schema (verified via live `sync-game-state`)

```json
{
  "id": "...", "phase": "lobby|playing|ended",
  "participants": [{"id","name","appearance","isBot","teamId","position","money",
                    "bankruptedAt","debtTo","connectivity","connectivityKickAt",
                    "offlineSince","timedVotekickAt","votekickedAt",
                    "clock":{"bankMs","autoActedTurns","turnsTaken","lastGrantTurnFrom"}}],
  "currentPlayerIndex": 0,
  "mapId": "classic",
  "blocks": [{"name","type":"corner|city|airport|company|bonus","price","ownerId",
              "isMortgaged","countryId","rentPrices","level","housePrice",
              "hotelPrice","companyType","cornerType","bonusType",
              "suspendedTurnsRemaining","suspensionAmount"}],
  "boardConfig": {"goReward":{"land":300,"pass":200},
                  "prisonBlockIndex":10,"goToPrisonBlockIndex":30,
                  "vacationBlockIndex":20},
  "dice": [1,1], "cubesRolledInTurn": false, "canPerformTurnActions": false,
  "doublesInARow": 0, "forceNoAnotherTurn": false,
  "teams": [], "votekickerIds": [],
  "turnClock": {"config":{...}, "turn":{"turnStartedAt","grantedMs","autoActing"}},
  "auction": null, "trades": [], "tradeCreatorIds": [],
  "bonusCards": {"treasure":{"cards":[...]}, ...},
  "vacationCash": 0, "settings": {...}, "stampedFlags": {...},
  "hostId": "...", "winnerId": null,
  "stats": {"turnsCount","startedAt","leaderboard","heatMap","netWorths",
            "prisonVisits","instrumentation"}
}
```

**Prison/vacation mechanics:** `blocks[prisonBlockIndex].suspendedTurnsRemaining`
is `{playerId: turnsLeft}`. Standing *on* the prison block ≠ imprisoned; only
this map marks real imprisonment (same for vacation). Escape: roll doubles,
`pay-out-of-prison` ($50), or `use-pardon-card`.

**Sync model:** `dice-rolled`/`turn-ended` carry only a `snapshot` *hash*, not
state. The SPA computes the same hash locally; on mismatch it emits
`request-sync {snapshot}` and receives `sync-game-state`. Since we can't
compute their hash, just send `{snapshot:""}` — the server always responds
with the full state (verified).

## Turn clock (verified live)

Each turn runs on a deadline the agent cannot ignore:

```
turnStartedAt + pausedMs + offlineMs + grace          -> bank starts draining
                + grantedMs + currentPlayer.bankMs    -> hard expiry
```

`turnClock.config` (server-fixed, not a room setting):

| field | default | meaning |
|---|---|---|
| `graceMs` | 20000 | free think time at turn start |
| `debtGraceMs` | 60000 | grace when a debt resolution is pending |
| `bankStartMs` / `bankMaxMs` | 60000 / 180000 | per-player reserve |
| `minRefillMs` / `maxRefillMs` | 6000 / 20000 | bank refill for acting quickly |
| `grantMs` / `grantCapPerTurnMs` | 60000 / 120000 | per-grant / per-turn grant cap |
| `grantCooldownTurns` | 1 | turns between a granter's grants |
| `removalAfterAutoActedTurns` | 2 | strikes before seat removal |

- Expiry ⇒ the server auto-acts (roll / end-turn) and sets
  `turn.autoActing`; if the player didn't self-act,
  `participant.clock.autoActedTurns += 1`. At the limit the player is
  removed (the SPA shows "Your time ran out" and `participants` drops them;
  spectators may keep watching).
- Acting yourself ⇒ `autoActedTurns` resets to 0 and `bankMs` is refilled
  (more for faster play), so a consistently quick player never dies — the
  bank is a buffer for occasional slow turns, not a hard per-turn cap.
- Auctions pause the clock (`turn.auctionPausedAt`, `pausedMs`).
- Verified live: when a human's clock gets low the server broadcasts
  `clock-time-requested {playerId}` on their behalf and **bots auto-grant**
  (+60s observed within ~100ms). In all-agent rooms, harnesses should
  auto-`grant-clock-time` on `clock-time-requested` events to keep every
  seat alive. Requests from a seat with `lastGrantTurnFrom` on cooldown
  are ignored.

The harness computes `turnExpiresInMs` from `turnStartedAt` + `pausedMs` +
`offlineMs` + `grace` + `grantedMs` + `bankMs` using the
`request-server-time` offset (verified to track the real countdown within
~1s), and falls back to roll/end-turn inside a configurable safety margin.

## Notes for agent harnesses

- Acks are the error channel: `{ok:false, code, message}` — surface these to the agent.
- `turnClock` drives per-turn timers; `request-clock-time`/`grant-clock-time` extend.
- `canBotsJoin:true` → server auto-adds bot participants (good for
  deterministic self-play evals). `join-game {bot}` needs a server-signed
  token — don't bother; `canBotsJoin` is the supported path.
- Entry routes: create (`/room/new`), share code (`/room/find/{code}`),
  matchmaking "Play" (`/room/find/{2|3|4}`).
- All money is integer USD; board is 40-block Monopoly-like (`blockIndex`,
  `propertyIndex` are the same 0–39 index space; cities have levels 0–5).
