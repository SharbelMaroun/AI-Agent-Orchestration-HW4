"""Render a block model as a fenced mermaid flowchart (task 7.008)."""

import re

from archlens.graphops.block_model import BlockModel


def _node_id(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "_", name)


def render_block_diagram(model: BlockModel, direction: str = "TD") -> str:
    """Render the block model as a fenced mermaid flowchart in the given direction."""
    lines = ["```mermaid", f"flowchart {direction}"]
    for block in model.blocks:
        lines.append(f'    {_node_id(block.name)}["{block.name} ({block.member_count})"]')
    for edge in model.edges:
        lines.append(f"    {_node_id(edge.source)} -->|{edge.weight}| {_node_id(edge.target)}")
    lines.append("```")
    return "\n".join(lines)
