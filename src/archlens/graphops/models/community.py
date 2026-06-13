"""Community model + membership cross-reference check (tasks 4.027-4.028)."""

from pydantic import BaseModel, ConfigDict


class Community(BaseModel):
    """A density-based community — never derived from folder paths (Part C p8)."""

    model_config = ConfigDict(extra="forbid")

    community_id: str
    label: str
    node_ids: list[str]
    inter_community_edge_count: int = 0


def check_membership(community: Community, known_ids: set[str]) -> None:
    """Raise if a community references a node id absent from the graph's node set."""
    unknown = [nid for nid in community.node_ids if nid not in known_ids]
    if unknown:
        raise ValueError(
            f"community {community.community_id!r} references unknown nodes: {unknown}"
        )
