"""graph.json parser returning a validated Graph aggregate (tasks 4.031-4.033)."""

import json
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import ValidationError

from ..graphops.errors import GraphParseError
from ..graphops.models.community import Community, check_membership
from ..graphops.models.edge import Edge
from ..graphops.models.hyperedge import Hyperedge, RationaleNode
from ..graphops.models.node import Node


@dataclass
class Graph:
    """The validated in-memory graph aggregate."""

    nodes: list[Node] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    communities: list[Community] = field(default_factory=list)
    hyperedges: list[Hyperedge] = field(default_factory=list)
    rationale_nodes: list[RationaleNode] = field(default_factory=list)

    @property
    def node_ids(self) -> set[str]:
        return {n.id for n in self.nodes} | {r.id for r in self.rationale_nodes}


def _build(items: list, model, where: str) -> list:
    out = []
    for index, raw in enumerate(items):
        try:
            out.append(model.model_validate(raw))
        except ValidationError as exc:
            raise GraphParseError(f"{where}[{index}]: {exc.errors()[0]['msg']}") from exc
    return out


def _load(source) -> dict:
    if isinstance(source, dict):
        return source
    if isinstance(source, str | Path):
        path = Path(source)
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise GraphParseError(f"cannot read graph.json at {path}: {exc}") from exc
    raise GraphParseError(f"unsupported graph source type: {type(source).__name__}")


def parse_graph(source) -> Graph:
    """Parse a graph.json path or dict into a validated Graph; raise GraphParseError on any issue."""
    data = _load(source)
    if not isinstance(data, dict):
        raise GraphParseError("graph.json root must be a JSON object")
    graph = Graph(
        nodes=_build(data.get("nodes", []), Node, "nodes"),
        edges=_build(data.get("edges", []), Edge, "edges"),
        communities=_build(data.get("communities", []), Community, "communities"),
        hyperedges=_build(data.get("hyperedges", []), Hyperedge, "hyperedges"),
        rationale_nodes=_build(data.get("rationale_nodes", []), RationaleNode, "rationale_nodes"),
    )
    known = graph.node_ids
    for community in graph.communities:
        try:
            check_membership(community, known)
        except ValueError as exc:
            raise GraphParseError(str(exc)) from exc
    return graph
