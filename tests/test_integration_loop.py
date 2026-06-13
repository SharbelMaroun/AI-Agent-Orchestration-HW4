"""Integration: one improvement-loop iteration increments loop_iteration by 1 (task 10.050)."""

from archlens.agents.stop_eval import make_stop_eval_node


def test_one_loop_iteration_increments_by_exactly_one():
    state = {
        "graph_snapshot": {"diff": {"dependency_loss": 0, "modularity_improved": False,
                                    "new_isolates": False}},
        "stop_eval": {"tests_green": True, "ruff_zero": True},
        "loop_iteration": 1,
    }
    out = make_stop_eval_node()(state)
    assert out["stop_eval"]["met"] is False
    assert out["loop_iteration"] == 2
