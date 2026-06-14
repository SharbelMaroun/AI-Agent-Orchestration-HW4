"""TDD tests for the stop-condition evaluator and the loop hard cap (10.027-10.029)."""

from langgraph.graph import END

from archlens.agents.routing import route_from_supervisor
from archlens.agents.stop_eval import make_stop_eval_node

_GOOD = {"dependency_loss": 0, "modularity_improved": True, "new_isolates": False}


def _state(diff=None, tests=True, ruff=True, iteration=0):
    return {
        "graph_snapshot": {"diff": diff or dict(_GOOD)},
        "stop_eval": {"tests_green": tests, "ruff_zero": ruff},
        "loop_iteration": iteration,
    }


def _verdict(**kw):
    return make_stop_eval_node()(_state(**kw))["stop_eval"]


def test_conditions_all_met_sets_met_true():
    assert _verdict()["met"] is True


def test_conditions_dependency_loss_blocks_met():
    assert _verdict(diff={**_GOOD, "dependency_loss": 2})["met"] is False


def test_conditions_no_modularity_improvement_blocks_met():
    assert _verdict(diff={**_GOOD, "modularity_improved": False})["met"] is False


def test_conditions_new_isolates_block_met():
    assert _verdict(diff={**_GOOD, "new_isolates": True})["met"] is False


def test_conditions_red_tests_block_met():
    assert _verdict(tests=False)["met"] is False


def test_conditions_ruff_violations_block_met():
    assert _verdict(ruff=False)["met"] is False


def test_hard_cap_increments_loop_iteration_when_unmet():
    out = make_stop_eval_node()(_state(tests=False, iteration=2))
    assert out["loop_iteration"] == 3


def test_hard_cap_routes_end_at_iteration_five():
    state = {"loop_iteration": 5, "target_repo": {}, "graph_snapshot": {}}
    assert route_from_supervisor(state) == END
