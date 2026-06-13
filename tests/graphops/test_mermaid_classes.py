"""TDD tests for the mermaid classDiagram renderer (tasks 7.015-7.016)."""

from pathlib import Path

from archlens.graphops.class_extractor import extract_classes
from archlens.graphops.class_relations import class_relations
from archlens.graphops.mermaid_classes import render_class_diagram

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "classes_pkg"


def _render() -> str:
    return render_class_diagram(extract_classes(FIXTURE), class_relations(FIXTURE))


def test_has_fenced_classdiagram_header():
    out = _render()
    assert out.startswith("```mermaid")
    assert "classDiagram" in out
    assert out.rstrip().endswith("```")


def test_renders_inheritance_arrow():
    assert "Shape <|-- Circle" in _render()


def test_renders_composition_arrows():
    out = _render()
    assert "Circle *-- Color" in out
    assert "Service *-- Repository" in out
