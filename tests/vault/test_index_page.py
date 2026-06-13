"""TDD tests for the index.md hub generator (tasks 5.021-5.022)."""

from archlens.vault.index_page import render_index


def test_read_first_banner_present(vault_graph, vault_cfg):
    index = render_index(vault_graph, vault_cfg)
    assert index.startswith("# Index")
    assert "Read this hub first" in index
    assert "at most 3" in index


def test_curated_start_here_has_two_to_three_links(vault_graph, vault_cfg):
    index = render_index(vault_graph, vault_cfg)
    start = index.split("## Start here")[1].split("## Communities")[0]
    links = [ln for ln in start.splitlines() if ln.strip().startswith("- [[")]
    assert 2 <= len(links) <= 3
    assert "[[hot]]" in start


def test_all_communities_linked(vault_graph, vault_cfg):
    index = render_index(vault_graph, vault_cfg)
    communities = index.split("## Communities")[1]
    assert "[[payments]]" in communities
    assert "[[auth]]" in communities
