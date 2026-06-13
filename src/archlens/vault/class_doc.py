"""Generate deliverables/CLASS_SCHEMA.md from the extracted class model (task 7.039)."""

from pathlib import Path

from archlens.graphops.class_extractor import extract_classes
from archlens.graphops.class_relations import class_relations
from archlens.graphops.mermaid_classes import render_class_diagram
from archlens.shared.constants import CLASS_SCHEMA_MD


def render_class_schema(source_root, version: str) -> str:
    """Render CLASS_SCHEMA.md: version header, classDiagram, inheritance/composition tables."""
    classes = extract_classes(source_root)
    relations = class_relations(source_root)
    inheritance = [r for r in relations if r.kind == "inheritance"]
    composition = [r for r in relations if r.kind == "composition"]
    lines = [
        "# Class Schema", "", f"Version: {version}", "",
        "## Class Diagram", "", render_class_diagram(classes, relations), "",
        "## Inheritance", "", "| Base | Derived |", "| --- | --- |",
        *[f"| {r.source} | {r.target} |" for r in inheritance],
        "", "## Composition", "", "| Owner | Part |", "| --- | --- |",
        *[f"| {r.source} | {r.target} |" for r in composition],
    ]
    return "\n".join(lines)


def write_class_schema(source_root, out_dir, version: str) -> Path:
    """Write CLASS_SCHEMA.md under out_dir and return its path."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / CLASS_SCHEMA_MD
    path.write_text(render_class_schema(source_root, version), encoding="utf-8")
    return path
