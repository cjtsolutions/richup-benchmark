"""Offline regression test for state.py against a real sync-game-state capture.

sample_game_state.json was captured live from richup.io on 2026-09-18
(mid-game: phase=playing, 4 participants, 40 blocks).
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from richup import state as st  # noqa: E402

GS = json.load(open(Path(__file__).parent / "sample_game_state.json"))["gameState"]


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


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("PASS", name)
    print("all tests passed")
