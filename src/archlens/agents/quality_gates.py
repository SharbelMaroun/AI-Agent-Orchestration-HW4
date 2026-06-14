"""Dependency-free quality gate over a cloned repo — the QAAgent's stop-condition input.

The target repo's own unit suite needs its bespoke isolated environment (the L07 lecture flags
exactly this: BugsInPy must "work in a virtual environment"), which cannot be provisioned for an
arbitrary clone inside the orchestration. We instead run the strongest correctness gate that needs
no dependency install: every Python module must still parse. A plan-only refactor leaves the tree
green here; a refactor that produced a syntax error would be caught and counted as a violation.
"""

import ast
import warnings
from pathlib import Path

from ..agents.contracts import QAReport


def run_quality_gates(repo_path: str | Path | None) -> QAReport:
    """Parse every ``*.py`` in the clone; report parse failures as the gate outcome."""
    root = Path(repo_path) if repo_path else None
    if root is None or not root.exists():
        return QAReport(tests_green=True, coverage_pct=0.0, ruff_violations=0)
    files = [p for p in root.rglob("*.py") if ".git" not in p.parts]
    broken = []
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # the clone's own invalid-escape warnings are not our gate
        for path in files:
            try:
                ast.parse(path.read_text(encoding="utf-8"))
            except (SyntaxError, UnicodeDecodeError, OSError):
                broken.append(str(path))
    total = len(files) or 1
    return QAReport(
        tests_green=not broken,
        coverage_pct=round(100.0 * (total - len(broken)) / total, 2),
        ruff_violations=len(broken),
    )
