"""TDD tests for the Phase 11 loop enums in shared/constants.py (task 11.004)."""

from archlens.shared.constants import EvidenceLevel, FixPriority, LoopVerdict, StopCondition


def test_fix_priority_covers_p1_through_p5():
    assert [p.value for p in FixPriority] == ["P1", "P2", "P3", "P4", "P5"]


def test_evidence_level_is_the_four_rung_ladder():
    assert [e.value for e in EvidenceLevel] == ["OBSERVED", "INFERRED", "EXTRACTED", "VALIDATED"]


def test_stop_condition_has_five_conditions():
    assert [s.value for s in StopCondition] == ["SC-1", "SC-2", "SC-3", "SC-4", "SC-5"]


def test_loop_verdict_is_continue_or_stop():
    assert {v.value for v in LoopVerdict} == {"CONTINUE", "STOP"}


def test_fix_priority_sorts_lexicographically_by_value():
    assert sorted([FixPriority.P3, FixPriority.P1, FixPriority.P2], key=lambda p: p.value) == [
        FixPriority.P1,
        FixPriority.P2,
        FixPriority.P3,
    ]
