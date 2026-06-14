"""Read-only graph helpers shared by the vault page generators (Phase 5)."""

from collections import defaultdict

from ..graphops.parser import Graph
from ..shared.constants import LOW_CONFIDENCE_FLOOR, EvidenceType


def degree_scores(graph: Graph) -> dict[str, int]:
    scores: dict[str, int] = defaultdict(int)
    for edge in graph.edges:
        scores[edge.src] += 1
        scores[edge.dst] += 1
    return dict(scores)


def community_of(graph: Graph) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for community in graph.communities:
        for node_id in community.node_ids:
            mapping[node_id] = community.label
    return mapping


def ranked_nodes(graph: Graph, top_n: int) -> list[tuple[str, int]]:
    ordered = sorted(degree_scores(graph).items(), key=lambda kv: (-kv[1], kv[0]))
    return ordered[:top_n]


def entry_points(graph: Graph) -> list[str]:
    indeg: dict[str, int] = defaultdict(int)
    outdeg: dict[str, int] = defaultdict(int)
    for edge in graph.edges:
        outdeg[edge.src] += 1
        indeg[edge.dst] += 1
    return sorted(n.id for n in graph.nodes if indeg[n.id] == 0 and outdeg[n.id] > 0)


def anomalies(graph: Graph) -> list:
    flagged = []
    for edge in graph.edges:
        ambiguous = edge.type is EvidenceType.AMBIGUOUS
        weak_inferred = edge.type is EvidenceType.INFERRED and edge.confidence < LOW_CONFIDENCE_FLOOR
        if ambiguous or weak_inferred:
            flagged.append(edge)
    return flagged


def connector_labels(graph: Graph, label: str) -> list[str]:
    members = {n for c in graph.communities if c.label == label for n in c.node_ids}
    of = community_of(graph)
    out: set[str] = set()
    for edge in graph.edges:
        if edge.src in members and of.get(edge.dst, label) != label:
            out.add(of[edge.dst])
        if edge.dst in members and of.get(edge.src, label) != label:
            out.add(of[edge.src])
    return sorted(out)
