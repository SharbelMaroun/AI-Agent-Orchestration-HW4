"""TestGate — run the target repo's suite and map the exit code to a verdict (task 11.027).

The suite runs via `uv run pytest` through the gatekeeper egress; exit code 0 is PASS, any
non-zero is FAIL. On FAIL the iteration commit is reverted (red-gate-to-rollback, task 11.028).
"""

from ..shared.gitops import revert_commit

PASS = "PASS"
FAIL = "FAIL"


def _gatekeeper_runner(command, cwd):
    from ..gatekeeper.gatekeeper import Gatekeeper

    return Gatekeeper().run_subprocess(command, cwd)


class TestGate:
    """Runs `uv run pytest` in the target repo via the gatekeeper; maps the exit code to PASS/FAIL."""

    __test__ = False  # not a pytest test class despite the Test* name

    def __init__(self, runner=None, command=("uv", "run", "pytest")):
        self._runner = runner or _gatekeeper_runner
        self._command = list(command)

    def verdict(self, repo_path) -> str:
        """Return PASS if the target suite exits 0, else FAIL."""
        return PASS if self._runner(self._command, repo_path).returncode == 0 else FAIL

    def passed(self, repo_path) -> bool:
        """True when the target suite passes."""
        return self.verdict(repo_path) == PASS


def gate_then_rollback(repo_path, gate: TestGate, commit: str = "HEAD") -> str:
    """Run the gate; on FAIL revert the iteration commit. Return the verdict."""
    verdict = gate.verdict(repo_path)
    if verdict == FAIL:
        revert_commit(repo_path, commit)
    return verdict
