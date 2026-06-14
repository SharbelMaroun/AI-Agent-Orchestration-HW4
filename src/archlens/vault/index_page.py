"""index.md hub generator — read-first banner + curated next reads (tasks 5.021-5.022, PRD §7.2)."""

from ..graphops.parser import Graph
from ..vault.config import VaultConfig
from ..vault.wikilinks import render_link


def render_index(graph: Graph, cfg: VaultConfig, project: str = "archlens-target") -> str:
    """Render the hub note: read-first banner, 2-3 curated links, full community map, artifacts."""
    labels = [c.label for c in graph.communities]
    lines = [
        "# Index",
        "",
        f"Project: {project}. Read this hub first, then open at most "
        f"{cfg.index_read_first_count} linked pages (Part B reading protocol).",
        "",
        "## Start here",
        "",
        f"- {render_link('hot')} - attention page: centrality, entry points, anomalies",
    ]
    for label in labels[: cfg.index_read_first_count - 1]:
        lines.append(f"- {render_link(label)} - community overview")
    lines += ["", "## Communities", ""]
    lines += [f"- {render_link(label)}" for label in labels]
    lines += ["", "## Artifacts", "", "- raw/graph.json", "- raw/REPORT.md"]
    return "\n".join(lines) + "\n"
