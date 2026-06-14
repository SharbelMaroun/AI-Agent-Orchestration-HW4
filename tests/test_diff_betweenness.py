"""TDD tests for betweenness-centrality delta between two snapshots (task 11.033)."""

from archlens.metrics.graph_diff import betweenness_delta


def _graph(nodes, edges):
    return {
        "nodes": [{"id": n, "type": "code", "source_file": f"{n}.py"} for n in nodes],
        "edges": [{"from": a, "to": b, "relation": "calls", "type": "EXTRACTED",
                   "confidence": 0.8, "source_file": f"{a}.py"} for a, b in edges],
    }


def test_betweenness_delta_drops_for_relieved_node():
    before = _graph(["a", "b", "c"], [("a", "b"), ("b", "c")])
    after = _graph(["a", "b", "c"], [("a", "b"), ("a", "c")])
    assert betweenness_delta(before, after)["b"] < 0


def test_betweenness_delta_zero_when_unchanged():
    graph = _graph(["a", "b", "c"], [("a", "b"), ("b", "c")])
    assert betweenness_delta(graph, graph)["b"] == 0.0
