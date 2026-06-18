"""Normalize real Graphify output into the canonical Graph aggregate (Phase 4 correction).

Handles the networkx node-link format `graphify update` emits (edges under `links`,
`source`/`target`, tier in `confidence`, numeric `confidence_score`, per-node `community`)
as well as our own canonical `from`/`to` schema used by the test fixtures.
"""

import json
from pathlib import Path

from ..graphops.models.community import Community
from ..graphops.models.edge import Edge
from ..graphops.models.hyperedge import Hyperedge
from ..graphops.models.node import Node
from ..graphops.parser import Graph
from ..shared.constants import (
    CONFIDENCE_MAX,
    CONFIDENCE_MIN,
    EXTRACTED_CONFIDENCE,
    EvidenceType,
    NodeType,
)

_FILE_TYPE = {
    "code": NodeType.CODE,
    "doc": NodeType.DOC,
    "document": NodeType.DOC,
    "test": NodeType.TEST,
    "rationale": NodeType.RATIONALE,
    "media": NodeType.MEDIA,
    "config": NodeType.CONFIG,
}
_TIER = {t.value: t for t in EvidenceType}
_TIER_DEFAULT = {
    EvidenceType.EXTRACTED: EXTRACTED_CONFIDENCE,
    EvidenceType.INFERRED: 0.75,
    EvidenceType.AMBIGUOUS: CONFIDENCE_MIN,
}


def _clamp(value: float) -> float:
    return max(CONFIDENCE_MIN, min(CONFIDENCE_MAX, value))


def _node(raw: dict) -> Node:
    file_type = raw.get("file_type") or raw.get("type") or "code"
    return Node(
        id=raw["id"],
        type=_FILE_TYPE.get(str(file_type), NodeType.CODE),
        source_file=raw.get("source_file", ""),
        label=raw.get("label"),
        source_location=raw.get("source_location"),
    )


def _tier(raw: dict) -> EvidenceType:
    value = raw.get("type")
    if value is None and isinstance(raw.get("confidence"), str):
        value = raw["confidence"]
    return _TIER.get(str(value), EvidenceType.INFERRED)


def _confidence(raw: dict, tier: EvidenceType) -> float:
    raw_c = raw.get("confidence")
    if isinstance(raw_c, int | float):
        value = _clamp(float(raw_c))
    elif "confidence_score" in raw:
        value = _clamp(float(raw["confidence_score"]))
    else:
        value = _TIER_DEFAULT[tier]
    return EXTRACTED_CONFIDENCE if tier is EvidenceType.EXTRACTED else value


def _edge(raw: dict) -> Edge:
    tier = _tier(raw)
    return Edge(
        src=raw.get("source", raw.get("from")),
        dst=raw.get("target", raw.get("to")),
        relation=str(raw.get("relation", "references")),
        type=tier,
        confidence=_confidence(raw, tier),
        source_file=raw.get("source_file", ""),
    )


def _hyperedge(raw: dict) -> Hyperedge:
    """Map a Graphify hyperedge (member ids under ``nodes``, plus label/score extras) to the model."""
    return Hyperedge(
        id=raw["id"],
        relation=raw["relation"],
        member_node_ids=raw.get("member_node_ids", raw.get("nodes", [])),
        source_file=raw.get("source_file", ""),
    )


def _communities(nodes_raw: list, data: dict) -> list[Community]:
    groups: dict = {}
    for node in nodes_raw:
        cid = node.get("community")
        if cid is not None:
            groups.setdefault(cid, []).append(node["id"])
    if groups:
        return [
            Community(community_id=str(cid), label=f"community-{cid}", node_ids=ids)
            for cid, ids in sorted(groups.items())
        ]
    return [Community.model_validate(c) for c in data.get("communities", [])]


def load_graphify_graph(source) -> Graph:
    """Normalize a Graphify graph.json (or our canonical schema) into the Graph aggregate."""
    if isinstance(source, dict):
        data = source
    else:
        data = json.loads(Path(source).read_text(encoding="utf-8"))
    nodes_raw = data.get("nodes", [])
    edges_raw = data.get("links", data.get("edges", []))
    return Graph(
        nodes=[_node(n) for n in nodes_raw],
        edges=[_edge(e) for e in edges_raw],
        communities=_communities(nodes_raw, data),
        hyperedges=[_hyperedge(h) for h in data.get("hyperedges", []) if "relation" in h],
    )
