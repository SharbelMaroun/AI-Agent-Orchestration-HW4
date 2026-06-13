"""Extract classes, methods, and attributes from Python sources via the ast module (7.012)."""

import ast
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ClassInfo:
    """A class parsed from a source tree."""

    name: str
    module: str
    methods: tuple[str, ...]
    attributes: tuple[str, ...]
    bases: tuple[str, ...]


def _files(root: Path) -> list[Path]:
    return [root] if root.is_file() else sorted(root.rglob("*.py"))


def _is_self_attr(target: ast.expr) -> bool:
    return (
        isinstance(target, ast.Attribute)
        and isinstance(target.value, ast.Name)
        and target.value.id == "self"
    )


def _attributes(cls: ast.ClassDef) -> tuple[str, ...]:
    names: list[str] = []
    for node in ast.walk(cls):
        if isinstance(node, ast.Assign):
            names += [t.attr for t in node.targets if _is_self_attr(t)]
        elif isinstance(node, ast.AnnAssign) and _is_self_attr(node.target):
            names.append(node.target.attr)
    return tuple(dict.fromkeys(names))


def extract_classes(root: str | Path) -> list[ClassInfo]:
    """Parse every class definition under ``root`` into ClassInfo records."""
    classes: list[ClassInfo] = []
    for file in _files(Path(root)):
        tree = ast.parse(file.read_text(encoding="utf-8"))
        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                methods = tuple(
                    n.name for n in node.body
                    if isinstance(n, ast.FunctionDef | ast.AsyncFunctionDef)
                )
                bases = tuple(ast.unparse(b) for b in node.bases)
                classes.append(ClassInfo(node.name, file.stem, methods, _attributes(node), bases))
    return classes
