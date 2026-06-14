"""Critical-path extraction and single-point-of-failure detection (tasks 6.028, 6.030)."""

import networkx as nx

from ..graphops.dto import Citation, SpofFinding
from ..shared.constants import CriticalRelation

_CRITICAL = frozenset(relation.value for relation in CriticalRelation)


def _critical_subgraph(graph: nx.DiGraph) -> nx.DiGraph:
    sub: nx.DiGraph = nx.DiGraph()
    for src, dst, relation in graph.edges(data="relation"):
        if relation in _CRITICAL:
            sub.add_edge(src, dst)
    return sub


def critical_paths(graph: nx.DiGraph) -> list[list[str]]:
    """Maximal paths composed entirely of critical-relation edges (source to sink)."""
    sub = _critical_subgraph(graph)
    sources = [node for node in sub if sub.in_degree(node) == 0]
    sinks = [node for node in sub if sub.out_degree(node) == 0]
    paths: list[list[str]] = []
    for source in sources:
        for sink in sinks:
            paths.extend(nx.all_simple_paths(sub, source, sink))
    return paths


def _edge_citation(graph: nx.DiGraph, src: str, dst: str) -> Citation:
    data = graph.edges[src, dst]
    return Citation(
        relation=data.get("relation", ""),
        confidence=data.get("confidence", 0.0),
        source_file=data.get("source_file", ""),
    )


def spof_detect(graph: nx.DiGraph) -> list[SpofFinding]:
    """Nodes lying on every critical path; each finding carries the per-hop citation chain."""
    paths = critical_paths(graph)
    if not paths:
        return []
    common: set[str] = set(paths[0])
    for path in paths[1:]:
        common &= set(path)
    findings = []
    for node in sorted(common):
        broken = sum(1 for path in paths if node in path)
        representative = next(path for path in paths if node in path)
        chain = tuple(
            _edge_citation(graph, representative[i], representative[i + 1])
            for i in range(len(representative) - 1)
        )
        findings.append(SpofFinding(node_id=node, broken_paths=broken, citations=chain))
    return findings
