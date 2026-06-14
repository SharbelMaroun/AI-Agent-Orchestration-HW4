"""hot.md generator — top centrality, entry points, anomalies (tasks 5.014-5.020, PRD §7.1).

Each section is capped at hot_top_n so hot.md stays within its line budget on large repos;
a node with no community renders a plain '-' (never an unresolved wikilink).
"""

from ..graphops.parser import Graph
from ..vault.config import VaultConfig
from ..vault.graphview import anomalies, community_of, entry_points, ranked_nodes
from ..vault.wikilinks import render_link


def _community_cell(of: dict, node_id: str) -> str:
    label = of.get(node_id)
    return render_link(label) if label else "-"


def _note(items: list, cap: int) -> str:
    return f"_(showing top {cap} of {len(items)})_"


def render_hot(graph: Graph, cfg: VaultConfig) -> str:
    """Render the three fixed hot.md sections; node rows link to their community page."""
    of = community_of(graph)
    entries = entry_points(graph)
    anoms = anomalies(graph)
    lines = [
        "# Hot",
        "",
        "## Top centrality nodes",
        "",
        "| Node | Degree | Community |",
        "|---|---|---|",
    ]
    for node_id, score in ranked_nodes(graph, cfg.hot_top_n):
        lines.append(f"| {node_id} | {score} | {_community_cell(of, node_id)} |")
    lines += ["", "## Entry points", ""]
    if len(entries) > cfg.hot_top_n:
        lines.append(_note(entries, cfg.hot_top_n))
    for node_id in entries[: cfg.hot_top_n]:
        lines.append(f"- {node_id} -> {_community_cell(of, node_id)}")
    lines += ["", "## Anomalies needing review", ""]
    if len(anoms) > cfg.hot_top_n:
        lines.append(_note(anoms, cfg.hot_top_n))
    lines += ["| Edge | Relation | Confidence | Source |", "|---|---|---|---|"]
    for edge in anoms[: cfg.hot_top_n]:
        lines.append(
            f"| {edge.src} -> {edge.dst} | {edge.relation} | {edge.confidence} | {edge.source_file} |"
        )
    return "\n".join(lines) + "\n"
