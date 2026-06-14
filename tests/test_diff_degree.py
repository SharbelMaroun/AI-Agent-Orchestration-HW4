"""TDD tests for per-node degree-delta between two graph.json snapshots (task 11.031)."""

from archlens.metrics.graph_diff import degree_delta


def _graph(nodes, edges):
    return {
        "nodes": [{"id": n, "type": "code", "source_file": f"{n}.py"} for n in nodes],
        "edges": [{"from": a, "to": b, "relation": "calls", "type": "EXTRACTED",
                   "confidence": 0.8, "source_file": f"{a}.py"} for a, b in edges],
    }


def test_degree_delta_reports_per_node_change():
    before = _graph(["a", "b", "c"], [("a", "b"), ("a", "c")])
    after = _graph(["a", "b", "c"], [("a", "b")])
    delta = degree_delta(before, after)
    assert delta["a"] == -1
    assert delta["c"] == -1
    assert delta["b"] == 0


def test_degree_delta_handles_new_node():
    before = _graph(["a", "b"], [("a", "b")])
    after = _graph(["a", "b", "d"], [("a", "b"), ("a", "d")])
    assert degree_delta(before, after)["d"] == 1
