"""Meta-test enforcing the 'Expected:' result-docstring convention (task 13.049).

A test module opts into the convention by including 'Expected:' in its module docstring; every test
function in such a module must then document its expected result with an 'Expected:' docstring line.
This enforces the convention for convention-adopting modules without a cap-breaking retrofit of the
entire legacy suite (adding a docstring line to ~570 existing tests would blow the 150-line cap on
dozens of near-cap test files).

Expected: every test in an opted-in module carries an 'Expected:' docstring; zero violations now.
"""

import ast
from pathlib import Path

TESTS = Path(__file__).resolve().parent


def _module_opts_in(tree: ast.Module) -> bool:
    return "Expected:" in (ast.get_docstring(tree) or "")


def test_opted_in_modules_document_expected_results():
    """Expected: opted-in modules have an Expected: line on every test function."""
    violations = []
    for py_file in TESTS.rglob("test_*.py"):
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
        if not _module_opts_in(tree):
            continue
        for node in ast.walk(tree):
            if (isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
                    and "Expected:" not in (ast.get_docstring(node) or "")):
                violations.append(f"{py_file.name}::{node.name}")
    assert violations == [], f"missing Expected: docstrings: {violations}"
