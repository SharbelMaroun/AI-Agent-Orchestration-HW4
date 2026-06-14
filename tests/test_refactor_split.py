"""TDD tests for RefactorFixes.split_module (task 11.018)."""

import ast
from pathlib import Path

from archlens.agents.refactor_fixes import RefactorFixes
from archlens.shared.constants import LINE_CAP
from archlens.shared.lines import effective_lines

_FUNC = "def f{i}(x):\n    y = x + {i}\n    z = y * 2\n    w = z - 1\n    return w"


def _write_big(tmp_path: Path, n: int = 40) -> Path:
    body = "\n\n".join(_FUNC.format(i=i) for i in range(n))
    mod = tmp_path / "big.py"
    mod.write_text("import os\nimport sys\n\n" + body + "\n", encoding="utf-8")
    return mod


def test_precondition_module_exceeds_cap(tmp_path):
    assert effective_lines(_write_big(tmp_path).read_text(encoding="utf-8")) > LINE_CAP


def test_split_produces_parts_each_within_cap(tmp_path):
    parts = RefactorFixes().split_module(_write_big(tmp_path))
    assert len(parts) >= 2
    for part in parts:
        assert effective_lines(part.read_text(encoding="utf-8")) <= LINE_CAP


def test_split_preserves_all_function_names(tmp_path):
    parts = RefactorFixes().split_module(_write_big(tmp_path))
    names = set()
    for part in parts:
        names |= {n.name for n in ast.parse(part.read_text(encoding="utf-8")).body
                  if isinstance(n, ast.FunctionDef)}
    assert names == {f"f{i}" for i in range(40)}


def test_split_facade_imports_each_part(tmp_path):
    mod = _write_big(tmp_path)
    parts = RefactorFixes().split_module(mod)
    facade = mod.read_text(encoding="utf-8")
    for part in parts:
        assert part.stem in facade
