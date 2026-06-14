"""Per-iteration git operations: feature branching and rollback (tasks 11.014, 11.016).

Every git invocation routes through the gatekeeper (the sole subprocess egress); this module
never spawns git directly. Branch names follow fix/iter-<NN>-<slug> (PRD_improvement_loop §5);
rollback is a history-preserving revert, never a reset --hard.
"""

import re
from pathlib import Path


def _slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "fix"


def _make_default_runner():
    from ..gatekeeper.gatekeeper import Gatekeeper

    gatekeeper = Gatekeeper()

    def _run(args: list[str], cwd: Path) -> str:
        return gatekeeper.git_local(args, cwd)

    return _run


class IterationBrancher:
    """Creates and checks out one feature branch per loop iteration in the target repo."""

    def __init__(self, repo_path, branch_prefix: str, runner=None):
        self._repo = Path(repo_path)
        self._prefix = branch_prefix
        self._runner = runner

    def _run(self, args: list[str]) -> str:
        if self._runner is None:
            self._runner = _make_default_runner()
        return self._runner(args, self._repo)

    def branch_name(self, iteration: int, slug: str) -> str:
        """Return the fix/iter-<NN>-<slug> name for an iteration."""
        return f"{self._prefix}-{iteration:02d}-{_slugify(slug)}"

    def create(self, iteration: int, slug: str) -> str:
        """Create and check out the iteration's feature branch; return its name."""
        name = self.branch_name(iteration, slug)
        self._run(["checkout", "-b", name])
        return name


def revert_commit(repo_path, commit: str = "HEAD", runner=None) -> str:
    """Roll back a commit with a history-preserving git revert; return the new HEAD sha."""
    run = runner or _make_default_runner()
    cwd = Path(repo_path)
    run(["revert", "--no-edit", commit], cwd)
    return run(["rev-parse", "HEAD"], cwd).strip()
