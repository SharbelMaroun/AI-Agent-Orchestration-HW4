"""Human-review queue for AMBIGUOUS and sub-floor edges, with JSON round-trip (task 6.036)."""

import json
from pathlib import Path

import networkx as nx

from ..graphops.dto import Citation, ReviewItem
from ..graphops.thresholds import thresholds
from ..shared.constants import EvidenceType


class ReviewQueue:
    """FIFO queue of ReviewItem entries, persisted to review_queue.json."""

    def __init__(self) -> None:
        self._items: list[ReviewItem] = []

    def enqueue(self, item: ReviewItem) -> None:
        self._items.append(item)

    def items(self) -> list[ReviewItem]:
        return list(self._items)

    def save(self, path: str | Path) -> None:
        payload = [
            {
                "src": item.src,
                "dst": item.dst,
                "reason": item.reason,
                "relation": item.citation.relation,
                "confidence": item.citation.confidence,
                "source_file": item.citation.source_file,
            }
            for item in self._items
        ]
        Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "ReviewQueue":
        queue = cls()
        for row in json.loads(Path(path).read_text(encoding="utf-8")):
            citation = Citation(row["relation"], row["confidence"], row["source_file"])
            queue.enqueue(ReviewItem(row["src"], row["dst"], row["reason"], citation))
        return queue


def build_review_queue(graph: nx.DiGraph, cfg: dict | None = None) -> ReviewQueue:
    """Enqueue AMBIGUOUS edges and below-floor edges in graph (FIFO) order."""
    floor = (cfg if cfg is not None else thresholds()).get("confidence_floor")
    queue = ReviewQueue()
    for src, dst, data in graph.edges(data=True):
        if data.get("type") == EvidenceType.AMBIGUOUS.value:
            reason = "ambiguous"
        elif data.get("confidence", 1.0) < floor:
            reason = "low_confidence"
        else:
            continue
        citation = Citation(data.get("relation", ""), data.get("confidence", 0.0),
                            data.get("source_file", ""))
        queue.enqueue(ReviewItem(src, dst, reason, citation))
    return queue
