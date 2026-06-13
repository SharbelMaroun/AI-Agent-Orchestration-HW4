"""wiki/ community page generator with cross-links (tasks 5.023-5.024, 5.026, PRD §7.3)."""

from pathlib import Path

from archlens.graphops.parser import Graph
from archlens.vault.frontmatter import render_frontmatter
from archlens.vault.graphview import connector_labels
from archlens.vault.layout import VaultLayout
from archlens.vault.wikilinks import render_link, slugify


def render_community(label: str, members: list[str], connectors: list[str]) -> str:
    """One frontmattered note per community; links back to index/hot and out to neighbors."""
    fm = render_frontmatter("community", "generated", "archlens-target")
    bridges = ", ".join(render_link(c) for c in connectors) or "none"
    body = [
        f"# Community: {label}",
        "",
        "Members: " + ", ".join(members),
        "",
        f"Bridges out: {bridges}",
        "",
        f"Navigate: {render_link('index')}, {render_link('hot')}",
    ]
    return fm + "\n".join(body) + "\n"


def write_community_pages(graph: Graph, layout: VaultLayout) -> list[Path]:
    layout.create()
    written = []
    for community in graph.communities:
        connectors = connector_labels(graph, community.label)
        text = render_community(community.label, community.node_ids, connectors)
        path = layout.wiki_dir / f"{slugify(community.label)}.md"
        path.write_text(text, encoding="utf-8")
        written.append(path)
    return written
