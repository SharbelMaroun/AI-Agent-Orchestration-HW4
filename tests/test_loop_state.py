"""TDD tests for the LoopState model (task 11.005)."""

import pytest
from pydantic import ValidationError

from archlens.agents.loop_state import AppliedFix, LoopState


def test_defaults_are_zeroed_and_empty():
    state = LoopState()
    assert state.iteration == 0
    assert state.applied_fixes == []
    assert state.branches == []
    assert state.metrics_snapshots == []


def test_record_fix_tracks_history_and_branch():
    state = LoopState()
    fix = AppliedFix(fix_id="f1", priority="P1", branch="fix/iter-01-spof", accepted=True)
    state.record_fix(fix)
    assert state.applied_fixes[0].fix_id == "f1"
    assert state.branches == ["fix/iter-01-spof"]


def test_record_fix_does_not_duplicate_branch():
    state = LoopState()
    fix = AppliedFix(fix_id="f1", priority="P1", branch="fix/iter-01-spof", accepted=False)
    state.record_fix(fix)
    state.record_fix(fix)
    assert state.branches == ["fix/iter-01-spof"]


def test_snapshot_appends_a_copy():
    state = LoopState()
    metrics = {"degree": 3}
    state.snapshot(metrics)
    metrics["degree"] = 99
    assert state.metrics_snapshots == [{"degree": 3}]


def test_at_cap_uses_max_iterations():
    assert LoopState(iteration=5).at_cap(5) is True
    assert LoopState(iteration=4).at_cap(5) is False


def test_unknown_key_rejected():
    with pytest.raises(ValidationError):
        LoopState(bogus=1)


def test_applied_fix_requires_all_fields():
    with pytest.raises(ValidationError):
        AppliedFix(fix_id="f1")
