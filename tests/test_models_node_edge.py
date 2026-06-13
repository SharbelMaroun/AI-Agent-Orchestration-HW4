"""TDD tests for the Node and Edge models (tasks 4.023-4.026)."""

import pytest
from pydantic import ValidationError

from archlens.graphops.models.edge import Edge
from archlens.graphops.models.node import Node

NODE = {"id": "a.py", "type": "code", "source_file": "a.py"}
EDGE = {
    "from": "a.py",
    "to": "b.py",
    "relation": "imports",
    "type": "INFERRED",
    "confidence": 0.8,
    "source_file": "a.py",
}


def test_node_parses_minimal():
    node = Node.model_validate(NODE)
    assert node.id == "a.py"
    assert node.type.value == "code"


def test_node_rejects_unknown_type():
    with pytest.raises(ValidationError):
        Node.model_validate({**NODE, "type": "widget"})


def test_node_requires_source_file():
    with pytest.raises(ValidationError):
        Node.model_validate({"id": "a.py", "type": "code"})


def test_edge_parses_from_to_aliases():
    edge = Edge.model_validate(EDGE)
    assert edge.src == "a.py" and edge.dst == "b.py"
    assert edge.relation == "imports"


def test_edge_rejects_confidence_below_floor():
    with pytest.raises(ValidationError):
        Edge.model_validate({**EDGE, "confidence": 0.50})


def test_edge_rejects_confidence_above_ceiling():
    with pytest.raises(ValidationError):
        Edge.model_validate({**EDGE, "confidence": 0.96})


def test_edge_accepts_boundary_values():
    low = Edge.model_validate({**EDGE, "confidence": 0.55})
    high = Edge.model_validate({**EDGE, "confidence": 0.95})
    assert low.confidence == 0.55
    assert high.confidence == 0.95


def test_edge_requires_source_file():
    payload = {k: v for k, v in EDGE.items() if k != "source_file"}
    with pytest.raises(ValidationError):
        Edge.model_validate(payload)


def test_edge_accepts_open_relation_vocabulary():
    # Graphify emits an open AST relation set; "contains" is valid, not a closed enum member.
    edge = Edge.model_validate({**EDGE, "relation": "contains"})
    assert edge.relation == "contains"


def test_extracted_edge_must_be_pinned_at_max_confidence():
    with pytest.raises(ValidationError):
        Edge.model_validate({**EDGE, "type": "EXTRACTED", "confidence": 0.8})
