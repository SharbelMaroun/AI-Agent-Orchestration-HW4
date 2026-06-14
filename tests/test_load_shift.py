"""TDD tests for the moved-vs-removed load detector (task 11.039, Part C SC-1)."""

from archlens.metrics.load_shift import dependencies_lost, load_migrated


def _graph(nodes, edges):
    return {
        "nodes": [{"id": n, "type": "code", "source_file": f"{n}.py"} for n in nodes],
        "edges": [{"from": a, "to": b, "relation": "calls", "type": "EXTRACTED",
                   "confidence": 0.8, "source_file": f"{a}.py"} for a, b in edges],
    }


_NODES = ["t", "a", "b", "c", "m"]
_BEFORE = _graph(_NODES, [("a", "t"), ("b", "t"), ("c", "t"), ("t", "m")])
_MIGRATED = _graph(_NODES, [("a", "m"), ("b", "m"), ("c", "m"), ("m", "t")])
_DISTRIBUTED = _graph(_NODES, [("a", "m"), ("b", "c"), ("c", "m")])


def test_load_migrated_true_when_neighbor_absorbs():
    assert load_migrated(_BEFORE, _MIGRATED, "t") is True


def test_load_migrated_false_when_distributed():
    assert load_migrated(_BEFORE, _DISTRIBUTED, "t") is False


def test_dependencies_lost_true_when_removed_not_moved():
    assert dependencies_lost(_BEFORE, _DISTRIBUTED, "t") is True


def test_dependencies_lost_false_when_migrated():
    assert dependencies_lost(_BEFORE, _MIGRATED, "t") is False
