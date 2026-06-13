"""TDD tests for shared/version.py (task 1.014)."""

from archlens.shared.version import VERSION, get_version


def test_version_constant_is_1_00():
    assert VERSION == "1.00"


def test_get_version_returns_constant():
    assert get_version() == VERSION


def test_package_dunder_version_matches():
    import archlens

    assert archlens.__version__ == "1.00"
    assert archlens.__all__
