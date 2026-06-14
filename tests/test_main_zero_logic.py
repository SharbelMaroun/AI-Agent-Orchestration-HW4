"""AST guard: src/main.py is a zero-business-logic CLI shim (task 13.026).

Expected: src/main.py contains only a docstring, imports, and the __main__ delegation guard; a
seeded computation, assignment, or function definition fails the test.
"""

import ast
from pathlib import Path

MAIN = Path(__file__).resolve().parents[1] / "src" / "main.py"
_ALLOWED = (ast.Import, ast.ImportFrom, ast.If, ast.Expr)


def test_main_has_no_business_logic():
    """Expected: every top-level node in main.py is an import, the docstring, or the guard."""
    tree = ast.parse(MAIN.read_text(encoding="utf-8"))
    unexpected = [type(node).__name__ for node in tree.body if not isinstance(node, _ALLOWED)]
    assert unexpected == [], f"unexpected top-level nodes in main.py: {unexpected}"


def test_main_guard_delegates_to_sdk_cli():
    """Expected: main.py imports main from archlens.__main__ (delegation, not logic)."""
    source = MAIN.read_text(encoding="utf-8")
    assert "from archlens.__main__ import main" in source
