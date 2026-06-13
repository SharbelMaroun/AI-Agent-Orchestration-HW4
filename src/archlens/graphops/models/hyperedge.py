"""Hyperedge and RationaleNode models (tasks 4.029-4.030)."""

from pydantic import BaseModel, ConfigDict

from archlens.shared.constants import RationaleSubtype, Relation


class Hyperedge(BaseModel):
    """One group-level claim over multiple nodes; never decomposed to pairwise edges (Part C p22)."""

    model_config = ConfigDict(extra="forbid")

    id: str
    relation: Relation
    member_node_ids: list[str]
    source_file: str


class RationaleNode(BaseModel):
    """A first-class WHY/TODO/NOTE node linked to the element it explains (Part C p15)."""

    model_config = ConfigDict(extra="forbid")

    id: str
    subtype: RationaleSubtype
    text: str
    rationale_for: str
