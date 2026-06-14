"""AST guard: external API client call sites appear only inside the gatekeeper (task 13.021).

Expected: zero anthropic/openai/httpx/requests call sites in src/archlens outside gatekeeper/; a
seeded `httpx.Client()` (or similar) anywhere else fails the test.
"""

import ast
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "archlens"
_CLIENT_MODULES = {"anthropic", "openai", "httpx", "requests"}


def _api_call_sites(tree: ast.AST) -> list[str]:
    sites = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            base = node.func.value
            if isinstance(base, ast.Name) and base.id in _CLIENT_MODULES:
                sites.append(f"{base.id}.{node.func.attr}")
    return sites


def test_no_api_call_sites_outside_gatekeeper():
    """Expected: no external-client call sites in any non-gatekeeper module."""
    offenders = []
    for py_file in SRC.rglob("*.py"):
        if "gatekeeper" in py_file.parts:
            continue
        sites = _api_call_sites(ast.parse(py_file.read_text(encoding="utf-8")))
        if sites:
            offenders.append((py_file.name, sites))
    assert offenders == [], f"API call sites outside gatekeeper: {offenders}"
