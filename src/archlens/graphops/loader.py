"""Load a graph.json into a networkx DiGraph for analysis (tasks 6.001-6.004)."""

import json
from pathlib import Path

import networkx as nx

from archlens.graphops.errors import GraphSchemaError
from archlens.shared.constants import Relation

_KNOWN_RELATIONS = frozenset(r.value for r in Relation)


def _read(source: dict | str | Path) -> dict:
    """Return the raw graph dict from a path, str, or already-parsed dict."""
    if isinstance(source, dict):
        return source
    path = Path(source)
    return json.loads(path.read_text(encoding="utf-8"))


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

    Node attributes kept: ``type``, ``source_file``.
    Edge attributes kept: ``relation``, ``type``, ``confidence``, ``source_file``.
    """
    data = _read(source)
    _validate(data)
    graph: nx.DiGraph = nx.DiGraph()
    for node in data.get("nodes", []):
        graph.add_node(
            node["id"],
            type=node.get("type"),
            source_file=node.get("source_file"),
        )
    for edge in data.get("edges", []):
        graph.add_edge(
            edge["from"],
            edge["to"],
            relation=edge.get("relation"),
            type=edge.get("type"),
            confidence=edge.get("confidence"),
            source_file=edge.get("source_file"),
        )
    return graph
