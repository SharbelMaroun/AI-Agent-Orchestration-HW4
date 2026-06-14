"""DRY audit: no duplicate function bodies, no triplicated try/except (8.036-8.038)."""

import ast
import hashlib
from collections import defaultdict
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "archlens"


def _body_key(node: ast.FunctionDef) -> str | None:
    stmts = node.body
    if stmts and isinstance(stmts[0], ast.Expr) and isinstance(getattr(stmts[0], "value", None), ast.Constant):
        stmts = stmts[1:]
    if len(stmts) < 2:
        return None
    return hashlib.md5("".join(ast.dump(s) for s in stmts).encode()).hexdigest()


def test_no_function_body_is_duplicated_across_files():
    bodies = defaultdict(set)
    for py_file in SRC.rglob("*.py"):
        for node in ast.walk(ast.parse(py_file.read_text(encoding="utf-8"))):
            if isinstance(node, ast.FunctionDef):
                key = _body_key(node)
                if key:
                    bodies[key].add(py_file.name)
    duplicates = {key: files for key, files in bodies.items() if len(files) >= 2}
    assert not duplicates, f"duplicate function bodies across files: {duplicates}"


def test_no_identical_try_except_in_three_or_more_files():
    patterns = defaultdict(set)
    for py_file in SRC.rglob("*.py"):
        for node in ast.walk(ast.parse(py_file.read_text(encoding="utf-8"))):
            if isinstance(node, ast.Try):
                handlers = tuple(ast.dump(handler) for handler in node.handlers)
                patterns[handlers].add(py_file.name)
    triplicated = {handlers: files for handlers, files in patterns.items() if len(files) >= 3}
    assert not triplicated, f"identical try/except in 3+ files: {triplicated}"
