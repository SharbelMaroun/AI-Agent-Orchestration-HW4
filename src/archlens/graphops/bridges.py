"""Structural bridges and community connectors — two distinct bridge senses (6.023, 6.025)."""

import networkx as nx

from archlens.graphops.dto import BridgeReport, Citation


def structural_bridges(graph: nx.DiGraph) -> list[tuple[str, str]]:
    """Edges whose removal disconnects the undirected projection, as sorted node pairs."""
    undirected = graph.to_undirected()
    pairs = [tuple(sorted((u, v))) for u, v in nx.bridges(undirected)]
    return sorted(pairs)


def community_connectors(
    graph: nx.DiGraph, communities: list[set[str]]
) -> list[tuple[str, str]]:
    """Directed edges whose endpoints fall in different communities, sorted for determinism."""
    member = {node: index for index, block in enumerate(communities) for node in block}
    crossing = [(u, v) for u, v in graph.edges if member.get(u) != member.get(v)]
    return sorted(crossing)


def _citation(graph: nx.DiGraph, u: str, v: str) -> Citation:
    data = graph.edges[u, v] if graph.has_edge(u, v) else graph.edges[v, u]
    return Citation(
        relation=data.get("relation", ""),
        confidence=data.get("confidence", 0.0),
        source_file=data.get("source_file", ""),
    )


def bridge_report(graph: nx.DiGraph, communities: list[set[str]]) -> BridgeReport:
    """Assemble a BridgeReport keeping structural bridges and connectors strictly separate."""
    structural = tuple(_citation(graph, u, v) for u, v in structural_bridges(graph))
    connector = tuple(_citation(graph, u, v) for u, v in community_connectors(graph, communities))
    return BridgeReport(structural=structural, connector=connector)
