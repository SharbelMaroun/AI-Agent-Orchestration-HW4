"""TDD tests for StopConditionEvaluator: 5 conditions + 5-iteration hard cap (task 11.041)."""

from archlens.agents.stop_evaluator import StopConditionEvaluator
from archlens.shared.constants import MAX_LOOP_ITERATIONS, LoopVerdict

_ALL_MET = {"SC-1": True, "SC-2": True, "SC-3": True, "SC-4": True, "SC-5": True}


def _graph(nodes, edges):
    return {
        "nodes": [{"id": n, "type": "code", "source_file": f"{n}.py"} for n in nodes],
        "edges": [{"from": a, "to": b, "relation": "calls", "type": "EXTRACTED",
                   "confidence": 0.8, "source_file": f"{a}.py"} for a, b in edges],
    }


_NODES = ["t", "a", "b", "c", "m"]
_BEFORE = _graph(_NODES, [("a", "t"), ("b", "t"), ("c", "t"), ("t", "m")])
# t sheds most load (degree 4 -> 1) but keeps one edge, so it is not orphaned (SC-3 holds).
_DISTRIBUTED = _graph(_NODES, [("a", "m"), ("b", "c"), ("c", "m"), ("t", "a")])


def test_decide_stops_when_all_conditions_met():
    out = StopConditionEvaluator().decide(_ALL_MET, iteration=1)
    assert out["verdict"] == LoopVerdict.STOP
    assert out["met"] is True


def test_decide_continues_when_a_condition_fails():
    out = StopConditionEvaluator().decide({**_ALL_MET, "SC-2": False}, iteration=1)
    assert out["verdict"] == LoopVerdict.CONTINUE
    assert out["met"] is False


def test_decide_stops_at_hard_cap_even_if_unmet():
    out = StopConditionEvaluator().decide({**_ALL_MET, "SC-4": False}, iteration=MAX_LOOP_ITERATIONS)
    assert out["verdict"] == LoopVerdict.STOP
    assert out["at_cap"] is True


def test_conditions_vector_has_all_five_keys():
    conds = StopConditionEvaluator().conditions(_BEFORE, _DISTRIBUTED, "t", True, True)
    assert set(conds) == {"SC-1", "SC-2", "SC-3", "SC-4", "SC-5"}


def test_conditions_reflect_graph_and_qa_signals():
    conds = StopConditionEvaluator().conditions(_BEFORE, _DISTRIBUTED, "t", True, True)
    assert conds["SC-1"] is True
    assert conds["SC-3"] is True
    assert conds["SC-4"] is True and conds["SC-5"] is True


def test_red_tests_block_sc4():
    conds = StopConditionEvaluator().conditions(_BEFORE, _DISTRIBUTED, "t", False, True)
    assert conds["SC-4"] is False
