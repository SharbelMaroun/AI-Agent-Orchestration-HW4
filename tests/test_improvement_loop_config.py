"""TDD tests for the improvement_loop block of config/setup.json (task 11.003)."""

from archlens.shared.config import load_setup


def test_improvement_loop_block_present_with_all_keys():
    il = load_setup().improvement_loop
    assert il.max_iterations == 5
    assert il.priority_order == ["P1", "P2", "P3", "P4", "P5"]
    assert il.allowed_evidence_levels == ["EXTRACTED", "VALIDATED"]
    assert il.branch_prefix


def test_priority_order_covers_p1_through_p5():
    assert set(load_setup().improvement_loop.priority_order) == {"P1", "P2", "P3", "P4", "P5"}


def test_max_iterations_matches_hard_cap_constant():
    from archlens.shared.constants import MAX_LOOP_ITERATIONS

    assert load_setup().improvement_loop.max_iterations == MAX_LOOP_ITERATIONS
