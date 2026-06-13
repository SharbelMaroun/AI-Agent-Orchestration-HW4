"""TDD tests for the wiki/ community page generator (tasks 5.023-5.024, 5.026)."""

from archlens.vault.community_pages import write_community_pages
from archlens.vault.layout import VaultLayout


def test_one_page_per_community(vault_graph, vault_cfg):
    paths = write_community_pages(vault_graph, VaultLayout(vault_cfg))
    assert len(paths) == len(vault_graph.communities)
    assert {p.name for p in paths} == {"payments.md", "auth.md"}


def test_page_has_frontmatter_members_and_crosslinks(vault_graph, vault_cfg):
    layout = VaultLayout(vault_cfg)
    write_community_pages(vault_graph, layout)
    text = (layout.wiki_dir / "payments.md").read_text(encoding="utf-8")
    assert text.startswith("---")
    for key in ("type: community", "status: generated", "project: archlens-target"):
        assert key in text
    assert "checkout" in text
    assert "[[auth]]" in text  # bridge to neighbor community
    assert "[[index]]" in text and "[[hot]]" in text  # back-links
