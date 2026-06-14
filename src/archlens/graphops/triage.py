"""Edge triage by evidence type and the confidence-threshold policy (tasks 6.032, 6.034)."""

import networkx as nx

from ..graphops.dto import Citation, TriageItem
from ..graphops.thresholds import thresholds
from ..shared.constants import EvidenceType


def _citation(data: dict) -> Citation:
    return Citation(
        relation=data.get("relation", ""),
        confidence=data.get("confidence", 0.0),
        source_file=data.get("source_file", ""),
    )


def triage_edges(graph: nx.DiGraph) -> dict[str, list[TriageItem]]:
    """Bucket every edge by its evidence type into EXTRACTED/INFERRED/AMBIGUOUS lists."""
    buckets: dict[str, list[TriageItem]] = {evidence.value: [] for evidence in EvidenceType}
    for src, dst, data in graph.edges(data=True):
        bucket = data["type"]
        buckets[bucket].append(TriageItem(src=src, dst=dst, bucket=bucket, citation=_citation(data)))
    return buckets


def confidence_policy(confidence: float, cfg: dict | None = None) -> str:
    """Label a confidence value against the config thresholds.

    ``strong`` at or above the strong threshold, ``human_review`` below the floor, otherwise
    ``needs_validation`` (at the floor up to but below strong).
    """
    cfg = cfg if cfg is not None else thresholds()
    floor = cfg.get("confidence_floor")
    strong = cfg.get("confidence_strong")
    if confidence < floor:
        return "human_review"
    if confidence >= strong:
        return "strong"
    return "needs_validation"
