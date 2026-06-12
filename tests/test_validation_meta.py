"""TDD tests for the has-tests and license validation checks (tasks 3.032, 3.034)."""

from pathlib import Path

from archlens.sdk.validation import check_has_tests, check_license

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_has_tests_detected_via_tests_directory():
    assert check_has_tests(FIXTURES / "mini_repo").passed


def test_has_tests_detected_via_pytest_config(tmp_path: Path):
    (tmp_path / "pytest.ini").write_text("[pytest]\n", encoding="utf-8")
    (tmp_path / "mod.py").write_text("X = 1\n", encoding="utf-8")
    assert check_has_tests(tmp_path).passed


def test_has_tests_rejects_no_tests_repo():
    result = check_has_tests(FIXTURES / "no_tests_repo")
    assert not result.passed and result.reason


def test_license_recognized_spdx_marker():
    result = check_license(FIXTURES / "mini_repo")
    assert result.passed and "MIT" in result.reason


def test_license_unrecognized_text_fails(tmp_path: Path):
    (tmp_path / "LICENSE").write_text("All rights reserved, proprietary.", encoding="utf-8")
    result = check_license(tmp_path)
    assert not result.passed and "unrecognized" in result.reason.lower()


def test_license_missing_fails_with_reason():
    result = check_license(FIXTURES / "no_license_repo")
    assert not result.passed and result.reason
