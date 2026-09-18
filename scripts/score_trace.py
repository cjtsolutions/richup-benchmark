"""Evaluate a JSONL trace from AgentHarness and compute benchmark metrics.

Usage:
    python scripts/score_trace.py trace.jsonl
    python scripts/score_trace.py traces/*.jsonl  # aggregate

Per-trace output:
    room_id       winner_id   won  steps  turns  t_fallbacks  t_timeouts
    action_ok%    final_money  final_net  duration_s  removed

Aggregate: averages across all traces.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_trace(path: str | Path) -> list[dict]:
    """Parse a JSONL trace file, returning a list of records."""
    records: list[dict] = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def net_worth(state: dict, player_id: str | None) -> float:
    """Estimate net worth from the final state.

    Uses the server's stats.netWorths last value when available, otherwise
    computes: money + sum(price * (1 + level) * (0.5 if mortgaged else 1)).
    """
    if not state:
        return 0.0
    me = None
    for p in state.get("players") or []:
        if p.get("id") == player_id:
            me = p
            break
    if me is None:
        return 0.0
    money = me.get("money") or 0
    # Try server-computed netWorths first
    net_worths = (state.get("stats") or {}).get("netWorths") or {}
    series = net_worths.get(player_id) if player_id else None
    if series and len(series) > 0:
        last = series[-1]
        if isinstance(last, (int, float)):
            return float(last)
    # Fallback: estimate from owned blocks
    blocks = state.get("blocks") or []
    prop_value = 0.0
    for b in blocks:
        if b.get("ownerId") == player_id:
            price = b.get("price") or 0
            level = b.get("level") or 0
            mortgaged = b.get("isMortgaged", False)
            mult = 1 + level
            if mortgaged:
                mult *= 0.5
            prop_value += price * mult
    return float(money + prop_value)


def score_trace(records: list[dict]) -> dict:
    """Compute metrics from a parsed trace."""
    meta: dict = {"room_id": None, "me": None, "winner_id": None}
    steps = 0
    actions = 0
    ok_actions = 0
    error_actions = 0
    timeout_fallbacks = 0
    decision_timeouts = 0
    removed = False
    final_state = None
    first_ts = None
    last_ts = None
    last_obs_ts = None
    decide_latencies_ms: list[float] = []
    action_error_codes: list[str] = []

    for rec in records:
        kind = rec.get("kind")
        ts = rec.get("t", 0)
        data = rec.get("data", {})

        if first_ts is None:
            first_ts = ts
        last_ts = ts

        if kind == "joined":
            meta["room_id"] = data.get("room_id")
            meta["me"] = data.get("player_id")
        elif kind == "observation":
            final_state = data
            last_obs_ts = ts
        elif kind == "action":
            steps += 1
            result = data.get("result", {})
            if isinstance(result, dict):
                if result.get("ok", False) or result.get("waited"):
                    ok_actions += 1
                else:
                    error_actions += 1
                    err = result.get("code") or result.get("error")
                    if err:
                        action_error_codes.append(str(err)[:80])
            elif result is None:
                ok_actions += 1
            actions += 1
            # estimate decide latency from time since last observation
            if last_obs_ts is not None and ts > last_obs_ts:
                decide_latencies_ms.append((ts - last_obs_ts) * 1000)
        elif kind == "clock_fallback":
            timeout_fallbacks += 1
        elif kind == "decision_timeout":
            decision_timeouts += 1
        elif kind == "removed":
            removed = True
        elif kind == "ended":
            meta["winner_id"] = data.get("winner_id")

    # final net worth
    player_id = meta.get("me")
    final_net = net_worth(final_state, player_id)
    final_money = 0
    if final_state:
        for p in final_state.get("players") or []:
            if p.get("id") == player_id:
                final_money = p.get("money") or 0
                break

    # turns: count dice-rolled events or action records with "roll_dice"
    turns = sum(
        1 for r in records
        if r.get("kind") == "action"
        and (r.get("data") or {}).get("action") == "roll_dice"
    )

    # leaderboard rank (1-based)
    rank = None
    if final_state:
        players = sorted(
            (p for p in final_state.get("players") or [] if not p.get("bankrupted")),
            key=lambda p: -(p.get("money") or 0),
        )
        for i, p in enumerate(players):
            if p.get("id") == player_id:
                rank = i + 1
                break

    duration_s = (last_ts - first_ts) if first_ts and last_ts else 0

    action_ok_pct = (ok_actions / actions * 100) if actions else 100.0
    avg_latency_ms = (
        sum(decide_latencies_ms) / len(decide_latencies_ms)
        if decide_latencies_ms
        else 0.0
    )

    return {
        "room_id": meta["room_id"],
        "player_id": meta["me"],
        "winner_id": meta["winner_id"],
        "won": meta.get("winner_id") and meta["me"] == meta["winner_id"],
        "rank": rank,
        "steps": steps,
        "turns": turns,
        "final_money": final_money,
        "final_net": final_net,
        "action_ok_pct": round(action_ok_pct, 1),
        "actions_total": actions,
        "action_errors": error_actions,
        "timeout_fallbacks": timeout_fallbacks,
        "decision_timeouts": decision_timeouts,
        "avg_decide_latency_ms": round(avg_latency_ms, 1),
        "duration_s": round(duration_s, 1),
        "removed": removed,
        "error_codes": action_error_codes[:10],
    }


def format_result(r: dict) -> str:
    """One-line summary."""
    won = "🏆" if r["won"] else " "
    rem = "🚫" if r["removed"] else " "
    return (
        f"{won}{rem} "
        f"room={r['room_id'] or '?'} "
        f"steps={r['steps']} "
        f"turns={r['turns']} "
        f"${r['final_money']} "
        f"net=${r['final_net']:.0f} "
        f"ok={r['action_ok_pct']}% "
        f"errs={r['action_errors']} "
        f"tf={r['timeout_fallbacks']} "
        f"dt={r['decision_timeouts']} "
        f"lat={r['avg_decide_latency_ms']:.0f}ms "
        f"dur={r['duration_s']:.0f}s"
        + (f" rank={r['rank']}" if r["rank"] else "")
        + (f" winner={r['winner_id'][:8]}" if r["winner_id"] else "")
    )


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Score richup-bench JSONL traces."
    )
    ap.add_argument("traces", nargs="+", help="JSONL trace file(s)")
    ap.add_argument("--json", action="store_true", help="Output JSON only")
    args = ap.parse_args()

    results: list[dict] = []
    for pattern in args.traces:
        for p in sorted(Path().glob(pattern)):
            records = load_trace(p)
            if not records:
                print(f"{p}: empty or invalid trace", file=sys.stderr)
                continue
            r = score_trace(records)
            r["file"] = str(p)
            results.append(r)

    if not results:
        print("No valid traces found.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(results, indent=2, default=str))
        return

    print()
    for r in results:
        print(f"  {r['file']}")
        print(f"    {format_result(r)}")
        if r["error_codes"]:
            print(f"    errors: {', '.join(r['error_codes'][:5])}")
    print()

    if len(results) > 1:
        # aggregate
        n = len(results)
        avg_steps = sum(r["steps"] for r in results) / n
        avg_turns = sum(r["turns"] for r in results) / n
        avg_money = sum(r["final_money"] for r in results) / n
        avg_net = sum(r["final_net"] for r in results) / n
        avg_ok = sum(r["action_ok_pct"] for r in results) / n
        avg_lat = sum(r["avg_decide_latency_ms"] for r in results) / n
        avg_dur = sum(r["duration_s"] for r in results) / n
        wins = sum(1 for r in results if r["won"])
        print(f"  === Aggregate ({n} traces) ===")
        print(f"    wins: {wins}/{n} ({wins / n * 100:.0f}%)")
        print(f"    avg steps: {avg_steps:.0f}")
        print(f"    avg turns: {avg_turns:.0f}")
        print(f"    avg final money: ${avg_money:.0f}")
        print(f"    avg net worth: ${avg_net:.0f}")
        print(f"    avg action ok: {avg_ok:.1f}%")
        print(f"    avg latency: {avg_lat:.0f}ms")
        print(f"    avg duration: {avg_dur:.0f}s")
        print()


if __name__ == "__main__":
    main()
