"""TDD test: the vault settings block loads via the typed config (task 5.003)."""

from archlens.shared.config import load_setup
from archlens.vault.config import VaultConfig


def test_vault_block_loads_with_all_keys(setup_json):
    cfg = load_setup(setup_json)
    assert isinstance(cfg.vault, VaultConfig)
    assert cfg.vault.hot_top_n == 10
    assert cfg.vault.raw_dir_name == "raw"
    assert cfg.vault.wiki_dir_name == "wiki"
    assert cfg.vault.index_read_first_count >= 1
