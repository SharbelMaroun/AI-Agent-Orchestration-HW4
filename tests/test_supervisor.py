"""TDD tests for supervisor routing decisions and the conditional router (10.007-10.009)."""

import pytest
from langgraph.graph import END

from archlens.agents.routing import route_from_supervisor
from archlens.agents.supervisor import supervise


def _bug(level="VALIDATED", status="open"):
    return {"from": "bughunter", "category": "SPOF", "level": level, "status": status,
            "relation": "calls", "confidence": 0.9, "source_file": "x.py"}


_ANALYZE = {"target_repo": {"local_path": "/x"}, "graph_snapshot": {"snapshot_id": 1}}
_QA = {"target_repo": {"x": 1}, "graph_snapshot": {"snapshot_id": 2, "post_fix": True},
       "findings": [_bug(status="fixed")]}

CASES = [
    ({}, "RepoAgent"),
    ({"target_repo": {"local_path": "/x"}}, "GraphAgent"),
    (_ANALYZE, "AnalystAgent"),
    ({**_ANALYZE, "findings": [{"from": "analyst", "category": "hub"}]}, "BugHunterAgent"),
    ({**_ANALYZE, "findings": [{"from": "analyst"}, _bug()]}, "RefactorAgent"),
    ({**_ANALYZE, "findings": [_bug(status="fixed")]}, "GraphAgent"),
    (_QA, "QAAgent"),
    ({**_QA, "stop_eval": {"tests_green": True, "ruff_zero": True}}, "MetricsAgent"),
    ({**_QA, "stop_eval": {"tests_green": True, "ruff_zero": True},
      "token_ledger": {"baseline_tokens": 1}}, "stop_eval"),
    ({**_ANALYZE, "stop_eval": {"met": True}}, "END"),
    ({**_ANALYZE, "loop_iteration": 5}, "END"),
]


@pytest.mark.parametrize("state,expected", CASES)
def test_supervisor_decision_branch(state, expected):
    assert supervise(state)["next"] == expected


def test_decision_carries_a_reason():
    assert supervise({})["reason"]


@pytest.mark.parametrize("state,expected", CASES)
def test_routing_maps_decision_to_node_or_end(state, expected):
    assert route_from_supervisor(state) == (END if expected == "END" else expected)
