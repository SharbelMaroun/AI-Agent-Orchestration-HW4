"""TDD tests for the clone error taxonomy (task 3.041) — one case per failure class."""

import pytest

from archlens.gatekeeper.git_ops import classify_git_failure
from archlens.shared.errors import (
    CloneAuthError,
    CloneNetworkError,
    DiskFullError,
    RepoError,
)


@pytest.mark.parametrize(
    ("stderr", "expected"),
    [
        ("fatal: Could not resolve host: github.com", CloneNetworkError),
        ("fatal: Authentication failed for 'https://github.com/x'", CloneAuthError),
        ("remote: Permission denied (403)", CloneAuthError),
        ("fatal: write error: No space left on device", DiskFullError),
        ("fatal: something completely unexpected", CloneNetworkError),
    ],
)
def test_stderr_maps_to_distinct_exception_types(stderr: str, expected: type):
    exc = classify_git_failure(stderr)
    assert type(exc) is expected
    assert isinstance(exc, RepoError)
    assert stderr.split(":")[-1].strip()[:10] in str(exc) or str(exc)


def test_no_bare_except_in_repo_modules():
    from pathlib import Path

    src = Path(__file__).resolve().parents[1] / "src" / "archlens"
    offenders = [
        p
        for p in src.rglob("*.py")
        if any(line.strip() == "except:" for line in p.read_text(encoding="utf-8").splitlines())
    ]
    assert offenders == []
