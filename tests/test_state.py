"""Offline regression test for state.py against a real sync-game-state capture.

sample_game_state.json was captured live from richup.io on 2026-09-18
(mid-game: phase=playing, 4 participants, 40 blocks).
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

import richup.events as ev

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from richup import state as st

with open(Path(__file__).parent / "sample_game_state.json") as _fh:
    GS = json.load(_fh)["gameState"]


def _client(phase="playing", self_id=None):
    c = MagicMock()
    c.game_state = GS
    c.room = {"id": GS["id"], "phase": phase, "settings": GS["settings"]}
    c.self_player_id = self_id or GS["participants"][0]["id"]
    c.self_player = GS["participants"][0]
    c.self_participant_id = "sock-participant-1"
    c.is_player = True
    c._room_id = GS["id"]
    c.events = []
    return c


def test_player_list():
    ps = st.player_list(GS)
    assert len(ps) == 4
    assert all("id" in p and "money" in p and "position" in p for p in ps)


def test_blocks():
    bs = st.blocks(GS)
    assert len(bs) == 40
    assert bs[0]["name"] == "Start"
    types = {b["type"] for b in bs}
    assert {"corner", "city", "airport", "company", "bonus"} <= types


def test_current_player():
    cur = st.current_player(GS)
    assert cur is GS["participants"][GS["currentPlayerIndex"]]


def test_prison_detection():
    me_id = GS["participants"][0]["id"]
    # nobody is imprisoned in this capture
    assert st.in_prison(GS, me_id) is False
    # simulate imprisonment
    gs2 = json.loads(json.dumps(GS))
    pidx = gs2["boardConfig"]["prisonBlockIndex"]
    gs2["blocks"][pidx]["suspendedTurnsRemaining"] = {me_id: 2}
    assert st.in_prison(gs2, me_id) is True
    assert st.suspended_turns(gs2, me_id) == 2


def test_summarize():
    c = _client()
    s = st.summarize(c)
    assert s["phase"] == "playing"
    assert len(s["players"]) == 4
    assert len(s["blocks"]) == 40
    assert s["self"]["playerId"] == GS["participants"][0]["id"]
    assert s["turn"]["isMyTurn"] == (
        GS["participants"][GS["currentPlayerIndex"]]["id"] == s["self"]["playerId"])


def test_available_actions():
    # make it my turn with dice not yet rolled
    c = _client()
    GS["canPerformTurnActions"] = True
    GS["cubesRolledInTurn"] = False
    for i, p in enumerate(GS["participants"]):
        if p["id"] == c.self_player_id:
            GS["currentPlayerIndex"] = i
    acts = st.available_actions(c)
    assert "roll_dice" in acts
    # property actions are gated on ownership — we own nothing yet
    assert "upgrade_city" not in acts
    assert "sell_property" not in acts

    # give ourselves a city -> upgrade becomes available
    me_id = c.self_player_id
    for b in GS["blocks"]:
        if b.get("type") == "city":
            b["ownerId"] = me_id
            break
    acts = st.available_actions(c)
    assert "sell_property" in acts
    assert "upgrade_city" in acts


def test_render_smoke():
    c = _client()
    txt = st.render(c)
    assert "phase=playing" in txt
    assert "board:" in txt
    assert "actions:" in txt


def test_available_actions_trade_responses():
    from richup.state import available_actions
    c = _client()
    me_id = c.self_player_id
    other_id = next(p["id"] for p in GS["participants"] if p["id"] != me_id)
    GS["trades"] = []
    acts = available_actions(c)
    assert "confirm_trade" not in acts
    assert "decline_trade" not in acts
    assert "delete_trade" not in acts
    GS["trades"] = [{"id": "t1", "initiatorId": other_id, "recipientId": me_id}]
    acts = available_actions(c)
    assert "confirm_trade" in acts
    assert "decline_trade" in acts
    assert "delete_trade" not in acts
    GS["trades"] = [{"id": "t2", "initiatorId": me_id, "recipientId": other_id}]
    acts = available_actions(c)
    assert "delete_trade" in acts
    assert "confirm_trade" not in acts
    GS["trades"] = []


def test_available_actions_bankrupt():
    from richup.state import available_actions
    c = _client()
    me_id = c.self_player_id
    for p in GS["participants"]:
        if p["id"] == me_id:
            p["debtTo"] = "some-creditor-id"
    acts = available_actions(c)
    assert "bankrupt" in acts
    for p in GS["participants"]:
        if p["id"] == me_id:
            p.pop("debtTo", None)


def test_available_actions_votekick():
    from richup.state import available_actions
    c = _client()
    acts = available_actions(c)
    assert "votekick" in acts


def test_available_actions_grant_clock():
    from richup.state import available_actions
    c = _client()
    me_id = c.self_player_id
    other_id = next(p["id"] for p in GS["participants"] if p["id"] != me_id)
    c.events.append({"t": 1000, "event": ev.CLOCK_TIME_REQUESTED, "data": {"playerId": other_id}})
    acts = available_actions(c)
    assert "grant_clock_time" in acts
    c.events.clear()
    c.events.append({"t": 1000, "event": ev.CLOCK_TIME_REQUESTED, "data": {"playerId": me_id}})
    acts = available_actions(c)
    assert "grant_clock_time" not in acts


def test_score_trace_smoke():
    import json
    import sys
    import tempfile
    trace = [
        {"t": 0, "kind": "joined", "data": {"room_id": "test-room", "player_id": "p1"}},
        {"t": 1, "kind": "observation", "data": {"players": [{"id": "p1", "money": 1500}], "blocks": []}},
        {"t": 2, "kind": "action", "data": {"action": "roll_dice", "args": {}, "result": {"ok": True}}},
        {"t": 3, "kind": "action", "data": {"action": "end_turn", "args": {}, "result": {"ok": True}}},
        {"t": 4, "kind": "ended", "data": {"winner_id": "p1"}},
    ]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        for rec in trace:
            f.write(json.dumps(rec) + "\n")
        tp = f.name
    try:
        sys.path.insert(0, "scripts")
        from score_trace import load_trace, score_trace
        recs = load_trace(tp)
        result = score_trace(recs)
        assert result["won"] is True
        assert result["room_id"] == "test-room"
        assert result["steps"] == 2
        assert result["action_ok_pct"] == 100.0
    finally:
        Path(tp).unlink(missing_ok=True)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
    print("all tests passed")
