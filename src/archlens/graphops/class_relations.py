"""Resolve inheritance and composition edges between extracted classes (task 7.014)."""

import ast
from dataclasses import dataclass
from pathlib import Path

from archlens.graphops.class_extractor import ClassInfo, extract_classes


@dataclass(frozen=True)
class ClassRelation:
    """A directed relation between two classes (inheritance or composition)."""

    source: str
    target: str
    kind: str


def _composition_targets(cls: ast.ClassDef, known: set[str]) -> set[str]:
    targets: set[str] = set()
    for node in ast.walk(cls):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in known:
            targets.add(node.func.id)
        elif (
            isinstance(node, ast.AnnAssign)
            and isinstance(node.annotation, ast.Name)
            and node.annotation.id in known
        ):
            targets.add(node.annotation.id)
    return targets


def class_relations(root: str | Path) -> list[ClassRelation]:
    """Inheritance (base <|-- derived) and composition (owner *-- part) edges among model classes."""
    classes: list[ClassInfo] = extract_classes(root)
    known = {c.name for c in classes}
    relations: list[ClassRelation] = []
    for info in classes:
        for base in info.bases:
            short = base.split(".")[-1]
            if short in known:
                relations.append(ClassRelation(short, info.name, "inheritance"))

    root_path = Path(root)
    files = [root_path] if root_path.is_file() else sorted(root_path.rglob("*.py"))
    for file in files:
        tree = ast.parse(file.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                for part in sorted(_composition_targets(node, known) - {node.name}):
                    relations.append(ClassRelation(node.name, part, "composition"))
    return relations
