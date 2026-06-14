"""TDD tests for the CLASS_SCHEMA.md generator (tasks 7.038-7.039)."""

from pathlib import Path

from archlens.vault.class_doc import render_class_schema, write_class_schema

CLASSES = Path(__file__).resolve().parents[1] / "fixtures" / "classes_pkg"


def test_has_version_header_and_classdiagram():
    text = render_class_schema(CLASSES, "1.00")
    assert "Version: 1.00" in text
    assert "classDiagram" in text


def test_has_inheritance_and_composition_tables():
    text = render_class_schema(CLASSES, "1.00")
    assert "## Inheritance" in text
    assert "## Composition" in text
    assert "| Base | Derived |" in text


def test_write_produces_class_schema_file(tmp_path):
    path = write_class_schema(CLASSES, tmp_path, "1.00")
    assert path.name == "CLASS_SCHEMA.md"
    assert "classDiagram" in path.read_text(encoding="utf-8")
