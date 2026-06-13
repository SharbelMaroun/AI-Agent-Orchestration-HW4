"""TDD tests for the is-Python and size-bounds validation checks (tasks 3.028, 3.030)."""

from pathlib import Path

from archlens.sdk.validation import check_is_python, check_size_bounds

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_is_python_passes_mini_repo():
    result = check_is_python(FIXTURES / "mini_repo", min_share=0.5)
    assert result.passed and result.name == "is_python"


def test_is_python_rejects_non_python_repo():
    result = check_is_python(FIXTURES / "non_python_repo", min_share=0.5)
    assert not result.passed and result.reason


def test_is_python_rejects_empty_repo(tmp_path: Path):
    result = check_is_python(tmp_path, min_share=0.5)
    assert not result.passed and "empty" in result.reason.lower()


def test_size_within_bounds_passes():
    result = check_size_bounds(FIXTURES / "mini_repo", 3, 50, max_size_mb=10)
    assert result.passed and result.name == "size_bounds"


def test_size_below_minimum_fails(tmp_path: Path):
    (tmp_path / "only.py").write_text("X = 1\n", encoding="utf-8")
    result = check_size_bounds(tmp_path, 3, 50, max_size_mb=10)
    assert not result.passed and result.reason


def test_size_above_maximum_fails(oversize_repo: Path):
    result = check_size_bounds(oversize_repo, 3, 50, max_size_mb=10)
    assert not result.passed and result.reason
