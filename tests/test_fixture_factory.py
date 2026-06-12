"""Smoke test: the git fixture factory builds a real repo with >= 1 commit (task 3.020)."""

import subprocess
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_git_repo_factory_builds_real_repo_with_commit(git_repo_factory):
    repo = git_repo_factory(FIXTURES / "mini_repo")
    assert (repo / ".git").is_dir()
    out = subprocess.run(
        ["git", "-C", str(repo), "rev-list", "--count", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert int(out.stdout.strip()) >= 1
