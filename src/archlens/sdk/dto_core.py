"""Frozen core SDK DTOs: repo spec, graph artifacts, analysis report (task 8.010)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RepoSpec:
    """The target repository to reverse-engineer."""

    url: str
    branch: str
    commit: str
    workdir: str


@dataclass(frozen=True)
class GraphArtifacts:
    """Paths to the artifacts a Graphify run produces."""

    graph_json: str
    graph_html: str
    report_md: str
    manifest: str


@dataclass(frozen=True)
class AnalysisReport:
    """A whole-graph analysis summary with the key architectural findings."""

    node_count: int
    edge_count: int
    community_count: int
    hubs: tuple[str, ...]
    bottlenecks: tuple[str, ...]
    spofs: tuple[str, ...]
