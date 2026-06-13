"""Vault test fixtures: a parsed 12-node graph and a tmp_path VaultConfig (task 5.005)."""

from pathlib import Path

import pytest

from archlens.graphops.parser import parse_graph
from archlens.vault.config import VaultConfig

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "vault" / "graph.json"


@pytest.fixture()
def vault_graph_path() -> Path:
    return FIXTURE


@pytest.fixture()
def vault_graph():
    return parse_graph(FIXTURE)


@pytest.fixture()
def vault_cfg(tmp_path: Path) -> VaultConfig:
    return VaultConfig(
        vault_root=str(tmp_path / "vault"),
        raw_dir_name="raw",
        wiki_dir_name="wiki",
        hot_top_n=10,
        index_read_first_count=3,
    )
