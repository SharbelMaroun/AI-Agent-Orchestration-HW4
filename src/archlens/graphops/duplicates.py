"""Duplicate detection that never auto-merges — it only routes to review (6.038, 6.040)."""

import networkx as nx

from archlens.graphops.dto import Citation, DuplicatePair, ReviewItem
from archlens.graphops.review_queue import ReviewQueue
from archlens.graphops.thresholds import thresholds
from archlens.shared.constants import Relation


def find_duplicates(graph: nx.DiGraph, cfg: dict | None = None) -> list[DuplicatePair]:
    """Flag semantically-similar edges whose confidence meets the duplicate threshold."""
    threshold = (cfg if cfg is not None else thresholds()).get("duplicate_similarity_threshold")
    pairs = []
    for src, dst, data in graph.edges(data=True):
        similar = data.get("relation") == Relation.SEMANTICALLY_SIMILAR_TO.value
        if similar and data.get("confidence", 0.0) >= threshold:
            citation = Citation(data["relation"], data["confidence"], data["source_file"])
            pairs.append(DuplicatePair(src, dst, data["confidence"], citation))
    return pairs


def route_duplicates_to_review(graph: nx.DiGraph, cfg: dict | None = None) -> ReviewQueue:
    """Route every duplicate finding into the review queue — never emit a merge action."""
    queue = ReviewQueue()
    for pair in find_duplicates(graph, cfg):
        queue.enqueue(ReviewItem(pair.node_a, pair.node_b, "duplicate", pair.citation))
    return queue
