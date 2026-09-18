"""Socket.IO event names for the richup.io wire protocol.

Grouped by domain; all names verified against the production bundle.
"""

# ---- namespaces -------------------------------------------------------------
NS_APP = "/api/app"
NS_GAME = "/api/game"
NS_LOBBY = "/api/lobby"

# engine.io (socket.io handshake) paths
SIO_PATH_APP = "api/app/socket.io/"
SIO_PATH_GAME = "api/game/socket.io/"  # shared by /api/game and /api/lobby

# ---- /api/lobby -------------------------------------------------------------
GET_LOBBY_ROOMS_LIST = "get-lobby-rooms-list"
LOBBY_ROOMS_LIST = "lobby-rooms-list"

# ---- room lifecycle (/api/game) ---------------------------------------------
ENTER_ROOM = "enter-room"                    # emit {roomId}
ENTERED_ROOM = "entered-room"                # on   {room, selfParticipantId, isPlayer, mutedPlayerIds, reportedPlayerIds, lostSeat}
JOIN_GAME = "join-game"                      # emit {name, appearance?, bot?, captchaToken?}
JOINED_GAME = "joined-game"                  # on   {selfPlayer}
PLAYER_JOINED = "player-joined"
PLAYER_LEFT = "player-left"                  # {playerId}
GAME_ERROR = "game-error"
GAME_ENDED = "game-ended"                    # {winnerId, coinRewardSeatId?}
ROOM_DELETED = "room-deleted"
ROOM_NOT_FOUND = "room-not-found"
VOTEKICK_PLAYER = "votekick-player"          # emit {playerId}
PLAYER_VOTEKICKED = "player-votekicked"      # {playerId, votingPlayerId, forced, snapshot}
NEW_VOTEKICK_REQUEST = "new-votekick-request"  # {votingPlayerId, snapshot}
HOST_KICK_PLAYER = "host-kick-player"        # emit {playerId}
PLAYER_HOST_KICKED = "player-host-kicked"    # {playerId, snapshot}
MUTE_PLAYER = "mute-player"                  # emit {playerId, muted}
REPORT_PLAYER = "report-player"              # emit {playerId, reason}
GRANT_CLOCK_TIME = "grant-clock-time"        # emit
REQUEST_CLOCK_TIME = "request-clock-time"    # emit
CLOCK_TIME_REQUESTED = "clock-time-requested"  # {playerId}
CLOCK_TIME_GRANTED = "clock-time-granted"    # {granterId, snapshot}
DO_BANKRUPT = "do-bankrupt"                  # emit
PLAYER_BANKRUPTED = "player-bankrupted"      # {playerId}
ROOM_RESTART = "room-restart"                # emit
UPDATE_GAME_ROOM = "update-game-room"        # emit partial settings
GAME_ROOM_UPDATED = "game-room-updated"
UPDATE_PLAYER_APPEARANCE = "update-player-appearance"  # emit {appearance}
PLAYER_APPEARANCE_UPDATED = "player-appearance-updated"  # {playerId, appearance}
PARTICIPANT_ACCOUNT_LINKED = "participant-account-linked"
PARTICIPANT_CONNECTIVITY_CHANGED = "participant-connectivity-changed"
TEAM_ACTION = "team-action"                  # emit
TEAM_UPDATED = "team-updated"

# ---- gameplay: sync / turn / dice -------------------------------------------
REQUEST_SYNC = "request-sync"                # emit {snapshot}
SYNC_GAME_STATE = "sync-game-state"          # on   {gameState, ...}
REQUEST_SERVER_TIME = "request-server-time"  # emit
START_GAME = "start-game"                    # emit
GAME_STARTED = "game-started"                # on   {participantsOrder:[{id},...]}
PLZ_ROLL_DICES = "plz-roll-dices"            # emit
DICE_ROLLED = "dice-rolled"                  # on   {dice:[d1,d2], snapshot, auto}
END_TURN = "end-turn"                        # emit
TURN_ENDED = "turn-ended"                    # on   {auto?}
PAY_OUT_OF_PRISON = "pay-out-of-prison"      # emit
PAID_OUT_OF_PRISON = "paid-out-of-prison"    # on
USE_PARDON_CARD = "use-pardon-card"          # emit
USED_PARDON_CARD = "used-pardon-card"        # on

# ---- gameplay: property / auction -------------------------------------------
PURCHASE_PROPERTY = "purchase-property"      # emit
PURCHASE_SUCCESS = "purchase-success"        # on   {blockIndex}
PURCHASE_FAILED = "purchase-failed"          # on
SELL_PROPERTY = "sell-property"              # emit {blockIndex}
PROPERTY_SOLD = "property-sold"              # on   {blockIndex}
UPGRADE_CITY = "upgrade-city"                # emit {blockIndex}
DOWNGRADE_CITY = "downgrade-city"            # emit {blockIndex}
CITY_LEVEL_CHANGED = "city-level-changed"    # on   {blockIndex, changeType}
START_AUCTION = "start-auction"              # emit
AUCTION_STARTED = "auction-started"          # on   {blockIndex, auto}
AUCTION_BID = "auction-bid"                  # emit {amount}
AUCTION_BADE = "auction-bade"                # on   {amount, bidderId, endsAt}
AUCTION_ENDED = "auction-ended"              # on   {blockIndex, price, buyerId}
MORTGAGE_PROPERTY = "mortgage-property"      # emit {propertyIndex}
PROPERTY_MORTGAGED = "property-mortgaged"    # on   {propertyIndex}
LIFT_PROPERTY_MORTGAGE = "lift-property-mortgage"  # emit {propertyIndex}
PROPERTY_MORTGAGE_LIFTED = "property-mortgage-lifted"  # on {propertyIndex}

# ---- gameplay: trading -------------------------------------------------------
CREATE_TRADE = "create-trade"                # emit {trade, negotiatedTradeId?}
TRADE_CREATED = "trade-created"              # on   {trade, negotiatedTradeId?}
CONFIRM_TRADE = "confirm-trade"              # emit {tradeId}
TRADE_CONFIRMED = "trade-confirmed"          # on   {tradeId}
DECLINE_TRADE = "decline-trade"              # emit {tradeId}
TRADE_DECLINED = "trade-declined"            # on   {tradeId}
DELETE_TRADE = "delete-trade"                # emit {tradeId}
TRADE_DELETED = "trade-deleted"              # on   {tradeId, auto?}
SET_TRADE_WATCH_STATE = "set-trade-watch-state"      # emit {tradeId, isWatching}
TRADE_WATCH_STATE_CHANGED = "trade-watch-state-changed"
SET_TRADE_CREATOR_STATE = "set-trade-creator-state"  # emit {isCreating}
TRADE_CREATOR_CHANGED = "trade-creator-changed"      # {playerId, isCreating}

# ---- chat / admin -------------------------------------------------------------
CHAT_SEND_MESSAGE = "chat:send-message"            # emit raw string (SPA verified: sendMessage(t) -> rr(e,oY,t))
CHAT_MESSAGE_RECEIVED = "chat:message-received"    # on {senderId, content}
CHAT_TYPING = "chat:typing"                        # emit
CHAT_PARTICIPANT_TYPING = "chat:participant-typing"
CHAT_SEND_TEAM_MESSAGE = "chat:send-team-message"      # emit raw string
CHAT_TEAM_MESSAGE_RECEIVED = "chat:team-message-received"
CHAT_SEND_ADMIN_MESSAGE = "chat:send-admin-message"    # emit raw string
CHAT_ADMIN_MESSAGE_RECEIVED = "chat:admin-message-received"
ADMIN_KICK_PARTICIPANT = "admin:kick-participant"  # emit {participantId, reason}
ADMIN_KICKED_PARTICIPANT = "admin:kicked-participant"

# ---- /api/app (social, optional) ----------------------------------------------
NEW_COIN_REWARD = "newCoinReward"
FRIENDSHIP_STATE_CHANGED = "friendshipStateChanged"
FRIEND_ROOM_INVITE = "friendRoomInvite"

# every event the client registers a listener for (used for catch-all logging)
KNOWN_SERVER_EVENTS = [
    ENTERED_ROOM, JOINED_GAME, PLAYER_JOINED, PLAYER_LEFT, GAME_ERROR,
    GAME_ENDED, ROOM_DELETED, ROOM_NOT_FOUND, PLAYER_VOTEKICKED,
    NEW_VOTEKICK_REQUEST, PLAYER_HOST_KICKED, PLAYER_BANKRUPTED,
    CLOCK_TIME_REQUESTED, CLOCK_TIME_GRANTED, GAME_ROOM_UPDATED,
    PLAYER_APPEARANCE_UPDATED, PARTICIPANT_ACCOUNT_LINKED,
    PARTICIPANT_CONNECTIVITY_CHANGED, TEAM_UPDATED,
    SYNC_GAME_STATE, GAME_STARTED, DICE_ROLLED, TURN_ENDED,
    PAID_OUT_OF_PRISON, USED_PARDON_CARD,
    PURCHASE_SUCCESS, PURCHASE_FAILED, PROPERTY_SOLD, CITY_LEVEL_CHANGED,
    AUCTION_STARTED, AUCTION_BADE, AUCTION_ENDED,
    PROPERTY_MORTGAGED, PROPERTY_MORTGAGE_LIFTED,
    TRADE_CREATED, TRADE_CONFIRMED, TRADE_DECLINED, TRADE_DELETED,
    TRADE_WATCH_STATE_CHANGED, TRADE_CREATOR_CHANGED,
    CHAT_MESSAGE_RECEIVED, CHAT_PARTICIPANT_TYPING,
    CHAT_TEAM_MESSAGE_RECEIVED, CHAT_ADMIN_MESSAGE_RECEIVED,
    ADMIN_KICKED_PARTICIPANT,
]

DEFAULT_ROOM_SETTINGS = {
    "maxPlayers": 4,
    "canBotsJoin": True,
    "isPrivate": True,
    "onlyUsers": False,
    "payDoubleRentWhenOwnFullSet": False,
    "vacationCash": False,
    "auction": False,
    "noRentPaymentsWhileInPrison": False,
    "mortgage": False,
    "startingCash": 1500,
    "evenBuild": True,
    "shufflePlayerOrder": True,
    "teams": {"enabled": False},
}
STARTING_CASH_OPTIONS = [500, 1000, 1500, 2000, 2500, 3000]
