"""Render extracted classes and relations as a fenced mermaid classDiagram (task 7.016)."""

from ..graphops.class_extractor import ClassInfo
from ..graphops.class_relations import ClassRelation

_ARROW = {"inheritance": "<|--", "composition": "*--"}


def render_class_diagram(classes: list[ClassInfo], relations: list[ClassRelation]) -> str:
    """Render a fenced mermaid classDiagram with class members and relation arrows."""
    lines = ["```mermaid", "classDiagram"]
    for info in classes:
        lines.append(f"    class {info.name} {{")
        for method in info.methods:
            lines.append(f"      +{method}()")
        lines.append("    }")
    for relation in relations:
        arrow = _ARROW.get(relation.kind, "-->")
        lines.append(f"    {relation.source} {arrow} {relation.target}")
    lines.append("```")
    return "\n".join(lines)
