"""TDD tests for the shared-flow and duplicate-flow detector (tasks 7.026-7.027)."""

from archlens.graphops.flow_detector import detect_duplicate_flows, detect_shared_flows
from archlens.graphops.req_matcher import Match

MATCHES = [
    Match("FR-01", "mod_a", 0.8),
    Match("FR-02", "mod_a", 0.7),
    Match("FR-03", "mod_b", 0.9),
]


def _dup_graph() -> dict:
    nodes = [{"id": n, "type": "code", "source_file": f"{n}.py"} for n in ("a", "b")]
    return {
        "nodes": nodes,
        "edges": [{"from": "a", "to": "b", "relation": "semantically_similar_to",
                   "type": "INFERRED", "confidence": 0.91, "source_file": "a.py"}],
    }


def test_module_serving_two_requirements_is_a_shared_flow():
    flows = {f.module for f in detect_shared_flows(MATCHES)}
    assert "mod_a" in flows
    assert "mod_b" not in flows


def test_shared_flow_lists_its_requirements():
    flows = {f.module: f for f in detect_shared_flows(MATCHES)}
    assert set(flows["mod_a"].req_ids) == {"FR-01", "FR-02"}


def test_duplicate_flow_at_threshold_detected():
    duplicates = detect_duplicate_flows(_dup_graph())
    assert any(d.similarity >= 0.91 for d in duplicates)
