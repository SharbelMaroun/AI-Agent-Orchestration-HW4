"""Generate deliverables/ARCHITECTURE.md from the block model (task 7.037)."""

from pathlib import Path

from ..graphops.block_model import build_block_model, top_block_model
from ..graphops.communities import load_communities
from ..graphops.mermaid_blocks import render_block_diagram
from ..shared.constants import ARCHITECTURE_MD
from ..vault.evidence_lint import enforce_evidence


def render_architecture(
    graph_source, version: str, direction: str = "TD", max_blocks: int | None = None
) -> str:
    """Render the ARCHITECTURE.md body: version header, mermaid block diagram, community table.

    When ``max_blocks`` is set and the graph has more communities than that, the diagram shows
    only the largest blocks for readability while the table keeps the full inventory.
    """
    communities = load_communities(graph_source)
    model = build_block_model(graph_source)
    shown = top_block_model(model, max_blocks) if max_blocks else model
    capped = len(shown.blocks) < len(model.blocks)
    narrative = [
        f"The codebase clusters into {len(communities)} communities [EXTRACTED].",
        "Inter-block dependencies mark the architecture's coupling points [INFERRED].",
    ]
    enforce_evidence(narrative)
    lines = ["# Architecture", "", f"Version: {version}", "", "## Block Diagram", ""]
    if capped:
        lines += [
            f"_Showing the {len(shown.blocks)} largest of {len(model.blocks)} "
            "communities; full inventory in the table below._",
            "",
        ]
    lines += [render_block_diagram(shown, direction), "",
              "## Communities", "", "| Community | Members |", "| --- | --- |"]
    ranked = sorted(communities, key=lambda c: (-len(c.members), c.label))
    lines += [f"| {c.label} | {len(c.members)} |" for c in ranked]
    lines += ["", "## Narrative", "", *[f"- {claim}" for claim in narrative]]
    return "\n".join(lines)


def write_architecture(
    graph_source, out_dir, version: str, direction: str = "TD", max_blocks: int | None = None
) -> Path:
    """Write ARCHITECTURE.md under out_dir and return its path."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / ARCHITECTURE_MD
    body = render_architecture(graph_source, version, direction, max_blocks)
    path.write_text(body, encoding="utf-8")
    return path
