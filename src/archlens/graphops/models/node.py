"""Node model for graph.json (PRD_graph_pipeline §4.1) — task 4.024.

Fields mirror real Graphify output: `label`, `source_location`, and `subtype` are optional
so a normalized Graphify node round-trips without loss.
"""

from pydantic import BaseModel, ConfigDict

from ...shared.constants import NodeType


class Node(BaseModel):
    """A graph node; source_file keeps every claim traceable (Part C p6)."""

    model_config = ConfigDict(extra="forbid")

    id: str
    type: NodeType
    source_file: str
    subtype: str | None = None
    label: str | None = None
    source_location: str | None = None
    metrics: dict[str, float] = {}
