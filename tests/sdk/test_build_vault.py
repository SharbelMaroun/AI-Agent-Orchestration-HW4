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


def test_build_vault_auto_populates_raw_layer_from_graph(setup_json, tmp_path):
    # The Karpathy raw layer is demonstrated end-to-end: the graph.json is ingested into raw/
    # with provenance and the index links the real file (no empty raw/, no dead link).
    cfg = load_setup(setup_json)
    cfg.vault.vault_root = str(tmp_path / "vault")
    layout = ArchLensSDK(setup=cfg).build_vault(FIXTURE)
    assert (layout.raw_dir / FIXTURE.name).is_file()
    assert f"- raw/{FIXTURE.name}" in layout.index_md.read_text(encoding="utf-8")
