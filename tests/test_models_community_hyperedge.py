"""TDD tests for Community, Hyperedge, and RationaleNode models (tasks 4.027-4.030)."""

import pytest

from archlens.graphops.models.community import Community, check_membership
from archlens.graphops.models.hyperedge import Hyperedge, RationaleNode


def _community(**kw):
    data = {"community_id": "c1", "label": "payments", "node_ids": ["a.py", "b.py"]}
    data.update(kw)
    return Community.model_validate(data)


def test_community_parses():
    community = _community()
    assert community.label == "payments"
    assert community.inter_community_edge_count == 0


def test_check_membership_accepts_known_ids():
    check_membership(_community(), {"a.py", "b.py", "c.py"})


def test_check_membership_rejects_unknown_id():
    with pytest.raises(ValueError, match="unknown nodes"):
        check_membership(_community(node_ids=["a.py", "ghost.py"]), {"a.py"})


def test_hyperedge_holds_three_members():
    he = Hyperedge.model_validate(
        {
            "id": "h1",
            "relation": "validates",
            "member_node_ids": ["a.py", "b.py", "c.py"],
            "source_file": "docs/PRD.md",
        }
    )
    assert len(he.member_node_ids) == 3


def test_rationale_node_links_to_an_edge_id():
    rn = RationaleNode.model_validate(
        {"id": "why-1", "subtype": "WHY", "text": "because", "rationale_for": "a.py->b.py"}
    )
    assert rn.subtype.value == "WHY"
    assert rn.rationale_for == "a.py->b.py"
