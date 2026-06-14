"""Shared rewiring helpers for structural refactors: import rewrite, seam, def extraction."""

import ast
from pathlib import Path


def rewrite_import(file_path, old_module: str, new_module: str) -> bool:
    """Rewrite `from <old> import ...` / `import <old>` to <new> in a file; return changed."""
    path = Path(file_path)
    changed = False
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith(f"from {old_module} import ") or stripped == f"import {old_module}":
            line = line.replace(old_module, new_module, 1)
            changed = True
        out.append(line)
    if changed:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return changed


def make_seam(source_path, dependents, suffix: str) -> Path:
    """Create a seam module re-exporting source's public API; rewire dependents onto it."""
    source = Path(source_path)
    seam = source.with_name(f"{source.stem}_{suffix}.py")
    seam.write_text(f"from {source.stem} import *  # seam over {source.stem}\n", encoding="utf-8")
    for dep in dependents:
        rewrite_import(dep, source.stem, seam.stem)
    return seam


def extract_def(text: str, name: str) -> tuple[str, str]:
    """Remove top-level function `name` from text; return (remaining_text, removed_source)."""
    for node in ast.parse(text).body:
        if isinstance(node, ast.FunctionDef) and node.name == name:
            segment = ast.get_source_segment(text, node) or ""
            lines = text.splitlines()
            del lines[node.lineno - 1: node.end_lineno]
            return "\n".join(lines).strip("\n"), segment
    return text, ""
