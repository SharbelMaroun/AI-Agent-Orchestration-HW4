"""TDD tests for IterationBrancher (task 11.013)."""

import subprocess
from pathlib import Path

from archlens.shared.gitops import IterationBrancher

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _current_branch(repo: Path) -> str:
    out = subprocess.run(
        ["git", "-C", str(repo), "branch", "--show-current"],
        capture_output=True, text=True, check=True,
    )
    return out.stdout.strip()


def test_branch_name_zero_pads_and_slugifies():
    brancher = IterationBrancher("x", "fix/iter")
    assert brancher.branch_name(1, "SPOF on Auth!") == "fix/iter-01-spof-on-auth"


def test_create_checks_out_fix_iter_branch(git_repo_factory):
    repo = git_repo_factory(FIXTURES / "mini_repo")
    name = IterationBrancher(repo, "fix/iter").create(1, "spof-auth")
    assert name == "fix/iter-01-spof-auth"
    assert _current_branch(repo) == name


def test_create_iteration_two_zero_pads(git_repo_factory):
    repo = git_repo_factory(FIXTURES / "mini_repo")
    name = IterationBrancher(repo, "fix/iter").create(2, "dup")
    assert name == "fix/iter-02-dup"
    assert _current_branch(repo) == "fix/iter-02-dup"
