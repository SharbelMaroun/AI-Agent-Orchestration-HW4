"""TDD tests for duplicate detection and the never-auto-merge guard (tasks 6.037-6.040)."""

from archlens.graphops.dto import ReviewItem
from archlens.graphops.duplicates import find_duplicates, route_duplicates_to_review
from archlens.graphops.loader import load_graph


def _dup_graph() -> dict:
    nodes = [{"id": n, "type": "code", "source_file": f"{n}.py"} for n in ("a", "b", "c", "d")]
    return {
        "nodes": nodes,
        "edges": [
            {"from": "a", "to": "b", "relation": "semantically_similar_to", "type": "INFERRED",
             "confidence": 0.91, "source_file": "a.py"},
            {"from": "c", "to": "d", "relation": "semantically_similar_to", "type": "INFERRED",
             "confidence": 0.909, "source_file": "c.py"},
        ],
    }


def test_duplicate_boundary_flags_091_and_ignores_0909():
    pairs = {(d.node_a, d.node_b) for d in find_duplicates(load_graph(_dup_graph()))}
    assert ("a", "b") in pairs
    assert ("c", "d") not in pairs


def test_duplicates_never_merge_only_route_to_review():
    queue = route_duplicates_to_review(load_graph(_dup_graph()))
    items = queue.items()
    assert all(isinstance(item, ReviewItem) for item in items)
    assert [(i.src, i.dst, i.reason) for i in items] == [("a", "b", "duplicate")]
