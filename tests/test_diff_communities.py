"""TDD tests for inter-community edge-count diff / modularity signal (task 11.035)."""

from archlens.metrics.graph_diff import inter_community_edge_delta, modularity_improved


def _graph(nodes, edges):
    return {
        "nodes": [{"id": n, "type": "code", "source_file": f"{n}.py"} for n in nodes],
        "edges": [{"from": a, "to": b, "relation": "calls", "type": "EXTRACTED",
                   "confidence": 0.8, "source_file": f"{a}.py"} for a, b in edges],
    }


_NODES = ["a", "b", "e", "c", "d", "f"]
_TRIANGLES = [("a", "b"), ("b", "e"), ("e", "a"), ("c", "d"), ("d", "f"), ("f", "c")]


def test_modularity_improves_when_cross_edges_drop():
    before = _graph(_NODES, [*_TRIANGLES, ("b", "c"), ("a", "d")])
    after = _graph(_NODES, [*_TRIANGLES, ("b", "c")])
    assert inter_community_edge_delta(before, after) < 0
    assert modularity_improved(before, after) is True


def test_modularity_not_improved_when_unchanged():
    graph = _graph(_NODES, [*_TRIANGLES, ("b", "c"), ("a", "d")])
    assert inter_community_edge_delta(graph, graph) == 0
    assert modularity_improved(graph, graph) is False
