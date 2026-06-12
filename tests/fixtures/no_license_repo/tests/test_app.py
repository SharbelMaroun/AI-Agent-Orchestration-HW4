"""Fixture test file (not collected by the ArchLens suite)."""

from no_license_repo.app import greet


def test_greet():
    assert greet("x") == "hello x"
