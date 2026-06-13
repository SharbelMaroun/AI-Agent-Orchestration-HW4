"""TDD tests for the YAML frontmatter renderer (tasks 5.008-5.009)."""

from archlens.vault.frontmatter import render_frontmatter


def test_frontmatter_starts_with_delimited_block():
    fm = render_frontmatter("community", "generated", "archlens-target")
    assert fm.startswith("---\n")
    assert fm.rstrip().endswith("---")


def test_frontmatter_contains_three_mandatory_keys():
    fm = render_frontmatter("community", "generated", "archlens-target")
    for key in ("type: community", "status: generated", "project: archlens-target"):
        assert key in fm
