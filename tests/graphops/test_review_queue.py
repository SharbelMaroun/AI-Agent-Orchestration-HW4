"""TDD tests for the AMBIGUOUS / sub-floor human-review queue (tasks 6.035-6.036)."""

from fixtures import build_star  # noqa: F401  (keeps fixtures importable for parity)

from archlens.graphops.loader import load_graph
from archlens.graphops.review_queue import ReviewQueue, build_review_queue


def _graph_with_review_edges() -> dict:
    return {
        "nodes": [{"id": n, "type": "code", "source_file": f"{n}.py"} for n in ("a", "b", "c", "d")],
        "edges": [
            {"from": "a", "to": "b", "relation": "uses", "type": "AMBIGUOUS",
             "confidence": 0.3, "source_file": "a.py"},
            {"from": "c", "to": "d", "relation": "mentions", "type": "INFERRED",
             "confidence": 0.5, "source_file": "c.py"},
        ],
    }


def test_ambiguous_and_subfloor_edges_enqueued_in_fifo_order():
    queue = build_review_queue(load_graph(_graph_with_review_edges()))
    assert [(i.src, i.dst, i.reason) for i in queue.items()] == [
        ("a", "b", "ambiguous"),
        ("c", "d", "low_confidence"),
    ]


def test_review_queue_survives_save_then_load(tmp_path):
    queue = build_review_queue(load_graph(_graph_with_review_edges()))
    path = tmp_path / "review_queue.json"
    queue.save(path)
    assert ReviewQueue.load(path).items() == queue.items()
