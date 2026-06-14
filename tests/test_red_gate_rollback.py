"""Integration test: a red target test triggers git revert and restores the baseline (11.028).

Per Guidelines V3 §6 the target suite execution is mocked (the gate verdict is injected);
git is real, so the revert and the byte-identical baseline restoration are genuine.
"""

import subprocess
from pathlib import Path
from types import SimpleNamespace

from archlens.agents.test_gate import FAIL, PASS, TestGate, gate_then_rollback

FIXTURES = Path(__file__).resolve().parent / "fixtures"
_IDENT = ["-c", "user.email=t@a.local", "-c", "user.name=T"]


def _git(repo: Path, *args, ident: bool = False) -> str:
    cmd = ["git", "-C", str(repo), *(_IDENT if ident else []), *args]
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()


def _tree(repo: Path) -> str:
    return _git(repo, "rev-parse", "HEAD^{tree}")


def _runner(code):
    def run(command, cwd):
        return SimpleNamespace(returncode=code, stdout="", stderr="")
    return run


def test_red_gate_reverts_and_restores_green_baseline(git_repo_factory):
    repo = git_repo_factory(FIXTURES / "mini_repo")
    baseline = _tree(repo)
    (repo / "broken.py").write_text("x = 1 / 0\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "iteration fix", ident=True)
    assert _tree(repo) != baseline

    verdict = gate_then_rollback(repo, TestGate(runner=_runner(1)), "HEAD")
    assert verdict == FAIL
    assert "Revert" in _git(repo, "log", "--oneline")
    assert _tree(repo) == baseline
    assert TestGate(runner=_runner(0)).verdict(repo) == PASS
