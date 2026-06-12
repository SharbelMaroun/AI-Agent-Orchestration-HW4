"""Fixture test file (not collected by the ArchLens suite)."""

from mini_pkg.core import add


def test_add():
    assert add(1, 2) == 3
