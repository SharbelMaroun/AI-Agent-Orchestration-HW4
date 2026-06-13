"""TDD tests for inheritance and composition detection between classes (tasks 7.013-7.014)."""

from pathlib import Path

from archlens.graphops.class_relations import ClassRelation, class_relations

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "classes_pkg"


def test_inheritance_edge_detected():
    assert ClassRelation("Shape", "Circle", "inheritance") in class_relations(FIXTURE)


def test_composition_via_instantiation():
    assert ClassRelation("Circle", "Color", "composition") in class_relations(FIXTURE)


def test_composition_via_type_annotation():
    assert ClassRelation("Service", "Repository", "composition") in class_relations(FIXTURE)


def test_no_edge_to_unknown_external_base():
    relations = class_relations(FIXTURE)
    names = {r.source for r in relations} | {r.target for r in relations}
    assert "UserList" not in names
    assert "collections.UserList" not in names
