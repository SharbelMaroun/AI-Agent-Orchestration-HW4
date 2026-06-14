"""TDD tests for isolated-component detection on the post-fix graph (task 11.037)."""

from archlens.metrics.graph_diff import new_isolated_components


def _graph(nodes, edges):
    return {
        "nodes": [{"id": n, "type": "code", "source_file": f"{n}.py"} for n in nodes],
        "edges": [{"from": a, "to": b, "relation": "calls", "type": "EXTRACTED",
                   "confidence": 0.8, "source_file": f"{a}.py"} for a, b in edges],
    }


def test_new_isolated_node_is_detected():
    before = _graph(["a", "b", "c"], [("a", "b"), ("b", "c")])
    after = _graph(["a", "b", "c"], [("a", "b")])
    assert new_isolated_components(before, after) is True


def test_no_new_isolated_components_when_still_connected():
    before = _graph(["a", "b", "c"], [("a", "b"), ("b", "c")])
    after = _graph(["a", "b", "c"], [("a", "b"), ("a", "c")])
    assert new_isolated_components(before, after) is False
