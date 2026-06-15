"""SDK refactor facade — apply a structural fix to the cloned repo (the single write entry point).

RefactorAgent calls this rather than touching files itself, so the SDK stays the one place that
mutates the target checkout. Dispatches by finding category to the Phase 11 RefactorFixes transforms.
"""

from pathlib import Path

from ..agents.refactor_fixes import RefactorFixes


class RefactorMixin:
    """Single-entry application of a structural fix to a cloned repo."""

    def apply_fix(self, finding: dict, repo_path: str) -> bool:
        """Apply the fix for ``finding`` under ``repo_path``; return True if a file was rewritten."""
        target = Path(repo_path or "") / finding.get("source_file", "")
        if not target.is_file():
            return False
        try:
            RefactorFixes().split_module(target)  # god_node/oversize -> split into <=cap parts
        except (OSError, ValueError, SyntaxError):
            return False
        return True
