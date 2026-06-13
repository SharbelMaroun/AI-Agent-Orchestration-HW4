"""TDD tests for the AST class extractor (tasks 7.011-7.012)."""

from pathlib import Path

from archlens.graphops.class_extractor import extract_classes

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "classes_pkg"


def _by_name() -> dict:
    return {c.name: c for c in extract_classes(FIXTURE)}


def test_extracts_all_class_names():
    assert {"Shape", "Circle", "Color", "Repository", "Service", "MyList"} <= set(_by_name())


def test_extracts_methods_including_init():
    by = _by_name()
    assert "__init__" in by["Shape"].methods
    assert "area" in by["Circle"].methods


def test_extracts_self_attributes():
    by = _by_name()
    assert "radius" in by["Circle"].attributes
    assert "color" in by["Circle"].attributes


def test_records_base_classes_and_module():
    by = _by_name()
    assert "Shape" in by["Circle"].bases
    assert by["Shape"].module == "shapes"


def test_records_dotted_external_base():
    assert _by_name()["MyList"].bases == ("collections.UserList",)
