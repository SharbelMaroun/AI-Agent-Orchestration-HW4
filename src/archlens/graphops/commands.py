"""Query, path, explain, and diff commands over the loaded graph (tasks 6.048, 6.050)."""

import networkx as nx

from ..graphops.communities import detect_communities
from ..graphops.dto import Citation, DiffReport
from ..graphops.graph_metrics import inter_community_edge_count


def _matches(data: dict, filters: dict) -> bool:
    return all(data.get(key) == value for key, value in filters.items())


def _citation(graph: nx.DiGraph, src: str, dst: str) -> Citation:
    data = graph.edges[src, dst]
    return Citation(data.get("relation", ""), data.get("confidence", 0.0), data.get("source_file", ""))


def query(graph: nx.DiGraph, node: dict | None = None, edge: dict | None = None) -> dict:
    """Filter nodes and edges by attribute, returning matching ids and edge pairs."""
    nodes = [n for n, data in graph.nodes(data=True) if _matches(data, node or {})]
    edges = [(u, v) for u, v, data in graph.edges(data=True) if _matches(data, edge or {})]
    return {"nodes": nodes, "edges": edges}


def path(graph: nx.DiGraph, src: str, dst: str) -> list[Citation]:
    """Return the shortest path from src to dst as a per-hop citation chain."""
    hops = nx.shortest_path(graph, src, dst)
    return [_citation(graph, hops[i], hops[i + 1]) for i in range(len(hops) - 1)]


def explain(graph: nx.DiGraph, src: str, dst: str) -> Citation:
    """Explain why an edge exists: its relation, confidence, and source_file."""
    return _citation(graph, src, dst)


def diff(before: nx.DiGraph, after: nx.DiGraph) -> DiffReport:
    """Before/after deltas feeding the improvement-loop stop conditions (Part C p21)."""
    lost = sum(
        1
        for u, v in before.edges
        if after.has_node(u) and after.has_node(v) and not after.has_edge(u, v)
    )
    isolated = sum(1 for node in after.nodes if after.degree(node) == 0)
    inter = inter_community_edge_count(after, detect_communities(after))
    return DiffReport(dependency_loss=lost, inter_community_after=inter, isolated_after=isolated)
