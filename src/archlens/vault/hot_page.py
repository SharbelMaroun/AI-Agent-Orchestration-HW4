"""hot.md generator — top centrality, entry points, anomalies (tasks 5.014-5.020, PRD §7.1)."""

from archlens.graphops.parser import Graph
from archlens.vault.config import VaultConfig
from archlens.vault.graphview import anomalies, community_of, entry_points, ranked_nodes
from archlens.vault.wikilinks import render_link


def render_hot(graph: Graph, cfg: VaultConfig) -> str:
    """Render the three fixed hot.md sections; node rows link to their community page."""
    of = community_of(graph)
    lines = [
        "# Hot",
        "",
        "## Top centrality nodes",
        "",
        "| Node | Degree | Community |",
        "|---|---|---|",
    ]
    for node_id, score in ranked_nodes(graph, cfg.hot_top_n):
        lines.append(f"| {node_id} | {score} | {render_link(of.get(node_id, 'unknown'))} |")
    lines += ["", "## Entry points", ""]
    for node_id in entry_points(graph):
        lines.append(f"- {node_id} -> {render_link(of.get(node_id, 'unknown'))}")
    lines += [
        "",
        "## Anomalies needing review",
        "",
        "| Edge | Relation | Confidence | Source |",
        "|---|---|---|---|",
    ]
    for edge in anomalies(graph):
        lines.append(
            f"| {edge.src} -> {edge.dst} | {edge.relation.value} | "
            f"{edge.confidence} | {edge.source_file} |"
        )
    return "\n".join(lines) + "\n"
