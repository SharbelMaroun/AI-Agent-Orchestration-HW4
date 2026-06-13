"""TDD tests for the vault layout builder (tasks 5.006-5.007)."""

from archlens.vault.layout import VaultLayout


def test_layout_creates_raw_and_wiki(vault_cfg):
    layout = VaultLayout(vault_cfg).create()
    assert layout.root.is_dir()
    assert layout.raw_dir.is_dir()
    assert layout.wiki_dir.is_dir()


def test_layout_named_artifact_paths(vault_cfg):
    layout = VaultLayout(vault_cfg)
    assert layout.hot_md.name == "hot.md"
    assert layout.index_md.name == "index.md"
    assert layout.log_md.name == "log.md"
