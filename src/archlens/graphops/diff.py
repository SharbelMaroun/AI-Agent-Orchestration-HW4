"""GraphDiff model and computation over two Graph runs (tasks 4.042-4.045)."""

from pydantic import BaseModel, ConfigDict

from ..graphops.parser import Graph


class GraphDiff(BaseModel):
    """Before/after deltas feeding the Part C p21 stop conditions (PRD §8)."""

    model_config = ConfigDict(extra="forbid")

    added_nodes: list[str] = []
    removed_nodes: list[str] = []
    added_edges: list[str] = []
    removed_edges: list[str] = []
    inter_community_edge_delta: int = 0
    new_isolated_components: list[str] = []
    bottleneck_dependency_loss: bool = False


def _edge_key(edge) -> tuple[str, str, str]:
    return (edge.src, edge.dst, edge.relation)


def _inter_count(graph: Graph) -> int:
    return sum(c.inter_community_edge_count for c in graph.communities)


def _isolated(graph: Graph) -> set[str]:
    connected = {e.src for e in graph.edges} | {e.dst for e in graph.edges}
    return {n.id for n in graph.nodes} - connected


def _dependency_loss(bottleneck: str, before: dict, after: dict) -> bool:
    removed = [k for k in before if k not in after and k[1] == bottleneck]
    added_sources = {k[0] for k in after if k not in before}
    return any(src not in added_sources for (src, _dst, _rel) in removed)


def compute_diff(before: Graph, after: Graph, bottleneck: str | None = None) -> GraphDiff:
    """Compute node/edge deltas, inter-community change, isolation, and bottleneck dependency loss."""
    before_nodes, after_nodes = {n.id for n in before.nodes}, {n.id for n in after.nodes}
    before_edges = {_edge_key(e): e for e in before.edges}
    after_edges = {_edge_key(e): e for e in after.edges}
    added, removed = set(after_edges) - set(before_edges), set(before_edges) - set(after_edges)
    return GraphDiff(
        added_nodes=sorted(after_nodes - before_nodes),
        removed_nodes=sorted(before_nodes - after_nodes),
        added_edges=[f"{k[0]}->{k[1]}:{k[2]}" for k in sorted(added)],
        removed_edges=[f"{k[0]}->{k[1]}:{k[2]}" for k in sorted(removed)],
        inter_community_edge_delta=_inter_count(after) - _inter_count(before),
        new_isolated_components=sorted(_isolated(after) - _isolated(before)),
        bottleneck_dependency_loss=(
            _dependency_loss(bottleneck, before_edges, after_edges) if bottleneck else False
        ),
    )
