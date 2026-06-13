"""Generate deliverables/ARCHITECTURE.md from the block model (task 7.037)."""

from pathlib import Path

from archlens.graphops.block_model import build_block_model
from archlens.graphops.communities import load_communities
from archlens.graphops.mermaid_blocks import render_block_diagram
from archlens.shared.constants import ARCHITECTURE_MD
from archlens.vault.evidence_lint import enforce_evidence


def render_architecture(graph_source, version: str, direction: str = "TD") -> str:
    """Render the ARCHITECTURE.md body: version header, mermaid block diagram, community table."""
    communities = load_communities(graph_source)
    diagram = render_block_diagram(build_block_model(graph_source), direction)
    narrative = [
        f"The codebase clusters into {len(communities)} communities [EXTRACTED].",
        "Inter-block dependencies mark the architecture's coupling points [INFERRED].",
    ]
    enforce_evidence(narrative)
    lines = [
        "# Architecture", "", f"Version: {version}", "",
        "## Block Diagram", "", diagram, "",
        "## Communities", "", "| Community | Members |", "| --- | --- |",
    ]
    lines += [f"| {c.label} | {len(c.members)} |" for c in communities]
    lines += ["", "## Narrative", "", *[f"- {claim}" for claim in narrative]]
    return "\n".join(lines)


def write_architecture(graph_source, out_dir, version: str, direction: str = "TD") -> Path:
    """Write ARCHITECTURE.md under out_dir and return its path."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / ARCHITECTURE_MD
    path.write_text(render_architecture(graph_source, version, direction), encoding="utf-8")
    return path
