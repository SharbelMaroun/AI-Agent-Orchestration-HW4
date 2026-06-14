"""TDD tests for the git-revert rollback helper (task 11.015)."""

import subprocess
from pathlib import Path

from archlens.shared.gitops import revert_commit

FIXTURES = Path(__file__).resolve().parent / "fixtures"
_IDENT = ["-c", "user.email=t@a.local", "-c", "user.name=T"]


def _git(repo: Path, *args, ident: bool = False) -> str:
    cmd = ["git", "-C", str(repo), *(_IDENT if ident else []), *args]
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()


def _tree_hash(repo: Path) -> str:
    return _git(repo, "rev-parse", "HEAD^{tree}")


def _commit_a_fix(repo: Path) -> None:
    (repo / "newfile.py").write_text("X = 1\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "planted fix", ident=True)


def test_revert_restores_pre_fix_tree(git_repo_factory):
    repo = git_repo_factory(FIXTURES / "mini_repo")
    before = _tree_hash(repo)
    _commit_a_fix(repo)
    assert _tree_hash(repo) != before
    revert_commit(repo)
    assert _tree_hash(repo) == before


def test_revert_adds_commit_never_resets(git_repo_factory):
    repo = git_repo_factory(FIXTURES / "mini_repo")
    base = int(_git(repo, "rev-list", "--count", "HEAD"))
    _commit_a_fix(repo)
    revert_commit(repo)
    assert int(_git(repo, "rev-list", "--count", "HEAD")) > base + 1
