"""Node model for graph.json (PRD_graph_pipeline §4.1) — task 4.024."""

from pydantic import BaseModel, ConfigDict

from archlens.shared.constants import NodeType


class Node(BaseModel):
    """A graph node; source_file is mandatory so every claim is traceable (Part C p6)."""

    model_config = ConfigDict(extra="forbid")

    id: str
    type: NodeType
    source_file: str
    subtype: str | None = None
    metrics: dict[str, float] = {}
