"""Load a graph.json into a networkx DiGraph for analysis (tasks 6.001-6.004)."""

import json
from pathlib import Path

import networkx as nx

from ..graphops.errors import GraphSchemaError
from ..shared.constants import EvidenceType, Relation

_KNOWN_RELATIONS = frozenset(r.value for r in Relation)
_EVIDENCE = frozenset(e.value for e in EvidenceType)


def _read(source: dict | str | Path) -> dict:
    """Return the raw graph dict from a path, str, or already-parsed dict."""
    if isinstance(source, dict):
        return source
    path = Path(source)
    return json.loads(path.read_text(encoding="utf-8"))


def _is_native(data: dict) -> bool:
    """True for Graphify's own networkx node-link export (edges under ``links``)."""
    return "links" in data and "edges" not in data


def _native_nodes(data: dict) -> list[dict]:
    """Map Graphify nodes (``file_type``) to the canonical node shape."""
    return [{"id": n["id"], "type": n.get("type") or n.get("file_type"),
             "source_file": n.get("source_file", "")} for n in data.get("nodes", [])]


def _native_edges(data: dict) -> list[dict]:
    """Map Graphify ``links`` (source/target, tier string, ``confidence_score``) to edges."""
    edges = []
    for link in data.get("links", []):
        tier = link.get("confidence")
        edges.append({
            "from": link.get("source"), "to": link.get("target"),
            "relation": link.get("relation", "references"),
            "type": tier if tier in _EVIDENCE else EvidenceType.AMBIGUOUS.value,
            "confidence": float(link.get("confidence_score", 1.0)),
            "source_file": link.get("source_file") or "graphify",
        })
    return edges


def _validate(data: dict) -> None:
    """Raise GraphSchemaError listing every edge that breaks the analysis schema."""
    node_ids = {n.get("id") for n in data.get("nodes", [])}
    offenders: list[str] = []
    for edge in data.get("edges", []):
        ref = f"{edge.get('from')}->{edge.get('to')}"
        if edge.get("from") not in node_ids or edge.get("to") not in node_ids:
            offenders.append(f"{ref}: endpoint is not a known node id")
        if not edge.get("source_file"):
            offenders.append(f"{ref}: missing source_file")
        confidence = edge.get("confidence")
        if not isinstance(confidence, int | float) or not 0.0 <= confidence <= 1.0:
            offenders.append(f"{ref}: confidence {confidence} outside [0.0, 1.0]")
        if edge.get("relation") not in _KNOWN_RELATIONS:
            offenders.append(f"{ref}: unknown relation {edge.get('relation')!r}")
    if offenders:
        raise GraphSchemaError("invalid graph: " + "; ".join(offenders))


def load_graph(source: dict | str | Path) -> nx.DiGraph:
    """Load a graph.json (path or dict) into a DiGraph, preserving node and edge attributes.

    Accepts both our canonical ``edges``/``from``/``to`` fixture schema and the real
    Graphify networkx node-link export (``links``/``source``/``target``). Strict schema
    validation runs only on the canonical form; the trusted Graphify export is normalized.

    Node attributes kept: ``type``, ``source_file``.
    Edge attributes kept: ``relation``, ``type``, ``confidence``, ``source_file``.
    """
    data = _read(source)
    if _is_native(data):
        nodes, edges = _native_nodes(data), _native_edges(data)
    else:
        _validate(data)
        nodes, edges = data.get("nodes", []), data.get("edges", [])
    graph: nx.DiGraph = nx.DiGraph()
    for node in nodes:
        graph.add_node(node["id"], type=node.get("type"), source_file=node.get("source_file"))
    for edge in edges:
        graph.add_edge(
            edge["from"], edge["to"],
            relation=edge.get("relation"), type=edge.get("type"),
            confidence=edge.get("confidence"), source_file=edge.get("source_file"),
        )
    return graph
