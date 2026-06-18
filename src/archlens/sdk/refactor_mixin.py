"""SDK refactor facade — apply a structural fix to the cloned repo (the single write entry point).

RefactorAgent calls this rather than touching files itself, so the SDK stays the one place that
mutates the target checkout. A bottleneck/god node is decoupled with an interface SEAM (its
dependents are rewired off it, which removes cross-community edges); with no known dependents it
falls back to splitting the oversized module.
"""

from pathlib import Path

from ..agents.guardrails import UndoRegistry
from ..agents.refactor_fixes import RefactorFixes
from ..graphops.errors import GraphSchemaError
from ..graphops.loader import load_graph


def _dependents(graph_json, finding: dict, repo: Path) -> list[str]:
    """Files of nodes that depend on the finding's node — the seam rewires these off the bottleneck."""
    if not graph_json:
        return []
    node_id = finding.get("id", "").removeprefix("validated-")
    try:
        graph = load_graph(graph_json)
    except (OSError, ValueError, GraphSchemaError):
        return []
    if node_id not in graph:
        return []
    own = finding.get("source_file")
    files = {graph.nodes[pred].get("source_file") for pred in graph.predecessors(node_id)}
    return [str(repo / f) for f in files if f and f != own and (repo / f).is_file()]


class RefactorMixin:
    """Single-entry application of a structural fix to a cloned repo."""

    def apply_fix(self, finding: dict, repo_path: str, graph_json=None) -> bool:
        """Apply the fix for ``finding`` under ``repo_path``; return True if a file was rewritten.

        Every file is snapshotted into an UndoRegistry before it is rewritten (the reversible-action
        guardrail), so ``undo_last_fix()`` can restore the checkout byte-for-byte if a gate later fails.
        """
        repo = Path(repo_path or "")
        target = repo / finding.get("source_file", "")
        if not target.is_file():
            return False
        dependents = _dependents(graph_json, finding, repo)
        undo = UndoRegistry()
        undo.snapshot(target)
        for dep in dependents:
            undo.snapshot(dep)
        self._undo = undo
        try:
            if dependents:
                RefactorFixes().break_bottleneck(target, dependents)  # interface seam (decouple)
            else:
                RefactorFixes().split_module(target)  # fallback: split the oversized module
        except (OSError, ValueError, SyntaxError):
            return False
        return True

    def undo_last_fix(self) -> bool:
        """Roll back every file the last apply_fix snapshotted; True if an undo registry existed."""
        undo = getattr(self, "_undo", None)
        if undo is None:
            return False
        undo.rollback_all()
        return True
