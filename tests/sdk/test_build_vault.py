"""TDD test: sdk.build_vault is the public entry to vault business logic (tasks 5.041-5.042)."""

from pathlib import Path

from archlens.sdk.sdk import ArchLensSDK
from archlens.shared.config import load_setup

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "vault" / "graph.json"


def test_build_vault_produces_artifacts(setup_json, tmp_path):
    cfg = load_setup(setup_json)
    cfg.vault.vault_root = str(tmp_path / "vault")
    layout = ArchLensSDK(setup=cfg).build_vault(FIXTURE)
    assert layout.hot_md.is_file()
    assert layout.index_md.is_file()
    assert len(list(layout.wiki_dir.glob("*.md"))) == 2
