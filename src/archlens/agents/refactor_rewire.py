"""Shared rewiring helpers for structural refactors: import rewrite, seam, def extraction."""

import ast
import re
from pathlib import Path

# Matches `from <dotted-or-relative module> import ...` and `import <dotted module>`.
_FROM = re.compile(r"^(\s*from\s+)([.\w]+)(\s+import\s+\S.*)$")
_IMPORT = re.compile(r"^(\s*import\s+)([.\w]+)(.*)$")


def _retarget(module: str, old: str, new: str) -> str | None:
    """Swap the last component to ``new`` when ``module`` is ``old`` or a dotted path ending in it."""
    if module == old or module.endswith(f".{old}"):
        return module[: len(module) - len(old)] + new
    return None


def rewrite_import(file_path, old_module: str, new_module: str) -> bool:
    """Rewrite imports of old_module (bare, relative ``.mod``, or dotted ``pkg.mod``) to new_module."""
    path = Path(file_path)
    changed = False
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        new_line = line
        for pattern in (_FROM, _IMPORT):
            match = pattern.match(line)
            if match:
                retargeted = _retarget(match.group(2), old_module, new_module)
                if retargeted is not None:
                    new_line = match.group(1) + retargeted + match.group(3)
                break
        changed = changed or new_line != line
        out.append(new_line)
    if changed:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return changed


def make_seam(source_path, dependents, suffix: str) -> Path:
    """Create a seam module re-exporting source's public API; rewire dependents onto it.

    The seam re-exports with a package-relative import when source sits in a package (an
    ``__init__.py`` sibling), so the seam works for both flat modules and package submodules.
    """
    source = Path(source_path)
    seam = source.with_name(f"{source.stem}_{suffix}.py")
    ref = f".{source.stem}" if (source.parent / "__init__.py").exists() else source.stem
    seam.write_text(f"from {ref} import *  # seam over {source.stem}\n", encoding="utf-8")
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
