"""Meta-test: every public function in src/archlens is referenced by a test (task 13.025).

Enumerates public module-level functions via AST and asserts each name appears somewhere in the
test corpus (transitively-tested helpers are referenced explicitly in test_public_callables.py).

Expected: zero public functions are unreferenced by the test suite.
"""

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "archlens"
TESTS = ROOT / "tests"


def _public_functions(py_file: Path) -> list[str]:
    tree = ast.parse(py_file.read_text(encoding="utf-8"))
    return [node.name for node in tree.body
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")]


def _test_corpus() -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in TESTS.rglob("test_*.py"))


def test_every_public_function_is_referenced():
    """Expected: each public src/archlens function name appears in at least one test module."""
    corpus = _test_corpus()
    missing = []
    for py_file in SRC.rglob("*.py"):
        if py_file.name == "__init__.py":
            continue
        for name in _public_functions(py_file):
            if name not in corpus:
                missing.append(f"{py_file.relative_to(SRC)}::{name}")
    assert missing == [], f"public functions never referenced in tests: {sorted(missing)}"
