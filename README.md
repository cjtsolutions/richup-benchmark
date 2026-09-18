# richup-bench

An agent harness + MCP server for [richup.io](https://richup.io) — a live,
browser-based multiplayer Monopoly-style economic game — built for evaluating
LLM agents on realistic long-horizon tasks: negotiation, trading, auctions,
money management, and imperfect-information play against bots and humans.

Reverse-engineered and built with the site owner's consent. The server offers
no special API — this client speaks the exact same protocol the web SPA does.

## What you get

| Piece | File | Role |
|---|---|---|
| Protocol doc | `PROTOCOL.md` | Wire-level reference (REST, socket.io events, payloads) |
| Client | `richup/client.py` | Cookie session + socket.io client, all actions/events, ack handling, auto state-sync |
| Captcha | `richup/captcha.py` | Mints real Turnstile tokens via a real Chrome window |
| State | `richup/state.py` | `summarize()` → structured state, `render()` → LLM-friendly board text, `available_actions()` |
| Session | `richup/session.py` | High-level bootstrap: create/join room, allow bots, start |
| MCP server | `richup/mcp_server.py` | 30 tools over stdio: lobby → gameplay → trade/chat |
| Harness | `richup/harness.py` | `AgentHarness.run()` episode loop + JSONL traces |
| Example agent | `examples/rule_agent.py` | Rule-based baseline player |

## Setup

```bash
python -m venv .venv && .venv/bin/pip install -r requirements.txt
# real Chrome is required for automated Turnstile minting:
#   patchright drives `channel="chrome"` (Google Chrome) headed on $DISPLAY.
```

## Quick start — play a game vs bots

```bash
.venv/bin/python examples/rule_agent.py --name BenchAgent --trace ep.jsonl
```

That single command does everything end-to-end:
creates a private room → mints a Turnstile token in a real Chrome window →
joins → enables `canBotsJoin` → server fills seats with bots → starts →
plays until `game-ended`, recording every observation/action to `ep.jsonl`.

Join an existing room instead:

```bash
.venv/bin/python examples/rule_agent.py --room x4sf7 --name BenchAgent   # room id
.venv/bin/python examples/rule_agent.py --code X4SF7 --name BenchAgent   # share code
.venv/bin/python examples/rule_agent.py --play 4 --name BenchAgent       # "Play": public matchmaking
```

`--play N` is the site's **Play button** — `GET /api/room/find/{2|3|4}`
matchmakes you into a public room where **real humans** may already be
seated. The host (whoever got there first) starts the game.

## MCP server

```json
{
  "mcpServers": {
    "richup": {
      "command": "/path/to/.venv/bin/python",
      "args": ["-m", "richup.mcp_server"],
      "cwd": "/path/to/richup-bench"
    }
  }
}
```

One server instance = one seat. Typical agent flow:
`create_room` → `update_settings` → `start_game` → loop
(`get_state`/`poll_events` → `roll_dice` → `buy_property` → `end_turn`) with
`create_trade`, `auction_bid`, `chat`, etc. as needed. Every mutating call
returns `{ok, result|error, state, available_actions}`.

For multiple agents in one room, run one MCP server (or harness) per seat —
they can share a `TurnstileProvider` or each mint their own token.

## Turnstile / captcha

`join-game` requires a Cloudflare Turnstile token (sitekey
`0x4AAAAAAC08XOgqbge2s3TZ`). Three ways to supply one, in precedence order:

1. **Automated (default)** — `TurnstileProvider` launches real Chrome
   (`patchright`, headed, `$DISPLAY`), loads richup.io, `eval`s the official
   `api.js`, renders a visible widget, and returns the token. Non-interactive
   pass in practice; retries up to 3×.
2. **Manual token** — solve Turnstile in your own browser on richup.io, then
   pass it:
   - `RICHUP_CAPTCHA_TOKEN=... .venv/bin/python examples/rule_agent.py`
   - or `--captcha-token ...` / `captcha_token=` on `create_room`/`join_room`.
   - Tokens are **single-use** and ~5 min TTL.
3. **Headless attempt** — `RICHUP_CAPTCHA_HEADLESS=1` (works sometimes;
   Cloudflare often insists on interaction → falls back to failure).

Environment knobs: `RICHUP_CAPTCHA_TIMEOUT` (default 90s),
`RICHUP_BRUNHILD_IP` (IPv4 edge for the IPv6-only challenge host —
see `captcha.py` docstring for why this exists).

## Writing your own agent

```python
class MyAgent:
    async def decide(self, obs: dict) -> dict:
        # obs = {"state": summarize(...), "board": render(...),
        #        "available_actions": [...], "new_events": [...]}
        if "roll_dice" in obs["available_actions"]:
            return {"action": "roll_dice"}
        return {"action": "wait"}

from richup.harness import AgentHarness
await AgentHarness(MyAgent(), name="MyAgent").run()  # -> {"winner_id", ...}
```

### LLM agents (OpenRouter / OpenAI / local)

`examples/llm_agent.py` plays any OpenAI-compatible chat model:

```bash
export OPENROUTER_API_KEY=sk-or-...
python examples/llm_agent.py --model anthropic/claude-sonnet-4
python examples/llm_agent.py --model openai/gpt-4o-mini --play 4     # humans
python examples/llm_agent.py --base-url http://localhost:11434/v1 \
    --model llama3.1 --api-key none                                # Ollama
```

Any model id the provider accepts works (`GET https://openrouter.ai/api/v1/models`
for the live list). The agent sends the board + actions + turn-clock each
step and parses `{"action","args"}` out of the reply, clamping to legal
actions and falling back to a safe move on garbage. `--decision-timeout`
bounds each call; slow answers get the clock fallback rather than a strike.

`examples/jev_agent.py` does the same for OpenRouter's **alpha decisions
API** (`typesafe/jev-1.13` et al.) — models that answer typed `noul` /
`choice` / `score` questions instead of chatting:

```bash
python examples/jev_agent.py                        # private bot room
python examples/jev_agent.py --play 4               # public matchmaking
```

Each step asks one `choice` over the legal actions plus at most one
follow-up for args (which block, what bid) — so most turns cost a single
API call.

Action vocabulary: `roll_dice, end_turn, buy_property, sell_property,
upgrade_city, downgrade_city, mortgage_property, lift_mortgage,
start_auction, auction_bid, create_trade, confirm_trade, decline_trade,
delete_trade, pay_out_of_prison, use_pardon_card, chat, bankrupt,
request_clock_time, grant_clock_time, votekick, host_kick, start_game,
update_game_room, sync, wait`.

`available_actions` surfaces all legal actions including trade responses
(`confirm_trade`/`decline_trade` when a trade targets you,
`delete_trade` when you initiated one), `grant_clock_time` when another
player has requested time, and `bankrupt` when you owe a debt.

### The turn clock (read this — it will kick a slow agent)

RichUp enforces a per-turn deadline: **20s grace, then your 60s time bank
drains; expiry = the server auto-acts for you and a second expiry removes
you from the game.** Acting yourself refills the bank (more for faster
play), so a consistently quick agent never dies. Full mechanics:
`PROTOCOL.md` "Turn clock".

The harness handles this for you:

- `obs["state"]["clock"]` exposes `turnExpiresInMs`, `myBankMs`,
  `myAutoActedTurns` — and the board text shows `clock: ... URGENT`.
- `decision_timeout_s` (default 60s) bounds one `decide()` call, clamped
  further by the live turn clock; if the agent can't answer in time the
  harness plays the server's own default (roll if unrolled else end-turn)
  instead of eating a strike, and records it in the trace
  (`timeout_fallbacks` in the episode result).
- `auto_request_clock` asks for time when your clock dips below
  `auto_request_below_ms` (15s); `auto_grant_clock` grants time to anyone
  who asks — in all-agent rooms every seat keeps the others alive.
- Verified live: at low clock the server broadcasts `clock-time-requested`
  for you and **bots auto-grant +60s**, so bot rooms are forgiving.
  Humans in public rooms usually are not — budget your `decide()` for
  ~10s there.

## Scoring runs

```bash
python scripts/score_trace.py traces/*.jsonl
```

Reads the JSONL trace files from `AgentHarness` and reports per-episode
metrics (winner, final net worth, action success rate, timeouts, decision
latency, etc.) plus an aggregate across multiple runs — letting you
compare agents or parameter sweeps.

Individual episode result:

```
  traces/rulebot-ep1.jsonl
    🏆  room=abc123 steps=127 turns=36 $1865 net=$3420 ok=94.5% errs=2 tf=0 dt=0 lat=823ms dur=312s rank=1
```

Aggregate (multiple files) adds averages and win rate.

## Good-citizen notes

- The owner consented to agent play, but be reasonable: a few concurrent
  rooms at most, don't spam room creation, don't harass human players in
  chat. Prefer `canBotsJoin` rooms for eval runs.
- Tokens are minted through real Chrome — don't parallelize token minting
  across many browsers.

## Limitations / TODO

- `appearance` must be one of the 12 palette hex colors (see
  `richup/session.py:APPEARANCE_PALETTE`); store-unlocked appearances are
  account-bound.
- Bots join "based on availability" — you can't pick bot count/skill.
- `trade` payloads accept `{initiatorId, recipientId, initiatorOffer{money,
  properties[]}, recipientOffer{...}, note}` — exact sub-schema mirrored from
  the SPA; see `PROTOCOL.md`.
- No reconnection-resume of a seat mid-game yet (reconnect re-enters the
  room; the server keeps your seat briefly via `connectivity` tracking).
- Chat/team/admin messages are sent as raw strings (verified from SPA
  bundles — `sendMessage(t)` → `rr(e,oY,t)`), not wrapped in `{content}`.
  The protocol doc (`PROTOCOL.md`) and event constants (`events.py`) have
  been corrected to reflect this.
- `score_trace.py` computes net worth from server `stats.netWorths` when
  available, falling back to a client-side estimate (money + property
  prices adjusted for levels and mortgages).
