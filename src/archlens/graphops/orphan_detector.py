"""Report graph modules that no requirement maps to, sorted by node degree (task 7.025)."""

from dataclasses import dataclass
from pathlib import Path

from ..graphops.loader import load_graph
from ..graphops.req_matcher import Match


@dataclass(frozen=True)
class Orphan:
    """A module with no matched requirement, carrying its graph degree."""

    module: str
    degree: int


def detect_orphans(graph_source: dict | str | Path, matches: list[Match]) -> list[Orphan]:
    """Return unmatched modules sorted by descending degree (then id for determinism)."""
    matched = {m.module for m in matches}
    graph = load_graph(graph_source)
    orphans = [Orphan(node, graph.degree(node)) for node in graph.nodes if node not in matched]
    orphans.sort(key=lambda o: (-o.degree, o.module))
    return orphans
