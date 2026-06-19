"""Three-tier guardrail action classifier and an undo registry (tasks 10.034-10.035).

read-only actions execute automatically; reversible actions require a registered undo path;
irreversible actions require human approval before they run.
"""

from enum import Enum
from pathlib import Path


class ActionTier(str, Enum):
    """The guardrail tier of a proposed action."""

    READ_ONLY = "read_only"
    REVERSIBLE = "reversible"
    IRREVERSIBLE = "irreversible"


_READ_ONLY = ("analyze", "read", "query", "inspect", "graph", "report", "view")
# Irreversible tier == requires human approval. Two families belong here: destructive VCS/deploy
# verbs, AND source-mutation verbs. Per ADR-009 every modification of the target's source code is
# irreversible-tier: an autonomous agent rewriting a human's repository must not run unsupervised,
# even though the SDK snapshots the file for rollback. The reversible tier is reserved for low-stakes
# writes to *derived* artifacts (vault notes, reports) that carry a registered undo path.
_IRREVERSIBLE = ("push", "delete", "force", "deploy", "publish", "drop", "rm ",
                 "apply", "refactor", "rewrite", "modify", "split", "edit", "patch")
_PATH_SEPARATORS = (" to ", " in ", " at ", " on ")


def _verb_phrase(action: str) -> str:
    """Return the action's verb phrase, excluding any trailing target path.

    Action strings are shaped ``"<verb...> to|in|at|on <path>"``. Classifying only the verb phrase
    keeps a *path* that merely contains a loaded word (e.g. ``delete_helper.py`` or ``deploy.py``)
    from spuriously escalating an otherwise reversible action — the tier must follow the verb, not
    the filename.
    """
    text = action.lower()
    for sep in _PATH_SEPARATORS:
        head, found, _ = text.partition(sep)
        if found:
            return head
    return text


def classify_action(action: str) -> ActionTier:
    """Classify an action string into its guardrail tier (by its verb, not its target path)."""
    verb = _verb_phrase(action)
    if any(token in verb for token in _IRREVERSIBLE):
        return ActionTier.IRREVERSIBLE
    if any(token in verb for token in _READ_ONLY):
        return ActionTier.READ_ONLY
    return ActionTier.REVERSIBLE


def requires_approval(action: str) -> bool:
    """True when the action is irreversible and needs human approval."""
    return classify_action(action) is ActionTier.IRREVERSIBLE


def requires_undo_path(action: str) -> bool:
    """True when the action is reversible and needs a registered undo path."""
    return classify_action(action) is ActionTier.REVERSIBLE


class UndoRegistry:
    """Snapshot file content before a reversible write so it can be restored byte-identically."""

    def __init__(self) -> None:
        self._snapshots: dict[str, str] = {}

    def snapshot(self, path: str | Path) -> None:
        self._snapshots[str(path)] = Path(path).read_text(encoding="utf-8")

    def rollback(self, path: str | Path) -> None:
        Path(path).write_text(self._snapshots[str(path)], encoding="utf-8")

    def rollback_all(self) -> None:
        """Restore every snapshotted file to its pre-write content (byte-identical)."""
        for path in list(self._snapshots):
            self.rollback(path)

    def paths(self) -> list[str]:
        """Return the snapshotted paths, for auditing which files a fix touched."""
        return sorted(self._snapshots)
