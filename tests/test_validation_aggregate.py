"""TDD tests for the aggregated validate_repo SDK function (tasks 3.036, 3.037)."""

from pathlib import Path

import pytest

from archlens.sdk.validation import validate_repo
from archlens.shared.config import ValidationBlock

FIXTURES = Path(__file__).resolve().parent / "fixtures"
VCFG = ValidationBlock(python_min_share=0.5, min_file_count=3, max_file_count=50)
EXPECTED_CHECKS = ["is_python", "size_bounds", "has_tests", "license"]


def test_result_lists_all_four_checks_with_reasons():
    result = validate_repo(FIXTURES / "mini_repo", VCFG, max_size_mb=10)
    assert [c.name for c in result.checks] == EXPECTED_CHECKS
    assert result.passed
    assert all(c.reason for c in result.checks)
    as_dict = result.as_dict()
    assert as_dict["passed"] is True and len(as_dict["checks"]) == 4


@pytest.mark.parametrize(
    ("fixture_name", "expected_failing_check"),
    [
        ("non_python_repo", "is_python"),
        ("no_tests_repo", "has_tests"),
        ("no_license_repo", "license"),
    ],
)
def test_each_negative_fixture_fails_exactly_its_check(fixture_name, expected_failing_check):
    result = validate_repo(FIXTURES / fixture_name, VCFG, max_size_mb=10)
    assert result.failing == [expected_failing_check]


def test_oversize_fixture_fails_only_size_bounds(oversize_repo: Path):
    result = validate_repo(oversize_repo, VCFG, max_size_mb=10)
    assert result.failing == ["size_bounds"]
