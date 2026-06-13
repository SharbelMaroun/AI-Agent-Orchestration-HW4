"""TDD tests for the full VaultBuilder pipeline and idempotent rebuild (5.037-5.040)."""

from pathlib import Path

from archlens.vault.builder import build_vault

GRAPHIFY = Path(__file__).resolve().parents[1] / "fixtures" / "graphify"


def _log_entries(layout) -> list[str]:
    return [ln for ln in layout.log_md.read_text(encoding="utf-8").splitlines() if ln.startswith("- ")]


def test_build_produces_all_artifacts(vault_graph, vault_cfg):
    layout = build_vault(
        vault_graph, vault_cfg, raw_sources=[GRAPHIFY / "full.json", GRAPHIFY / "REPORT.md"]
    )
    assert layout.hot_md.is_file()
    assert layout.index_md.is_file()
    assert layout.log_md.is_file()
    assert (layout.raw_dir / "full.json").is_file()
    assert len(list(layout.wiki_dir.glob("*.md"))) == 2


def test_idempotent_rebuild(vault_graph, vault_cfg):
    layout = build_vault(vault_graph, vault_cfg)
    hot1, index1 = layout.hot_md.read_bytes(), layout.index_md.read_bytes()
    wiki1 = {p.name: p.read_bytes() for p in layout.wiki_dir.glob("*.md")}
    entries1 = len(_log_entries(layout))
    build_vault(vault_graph, vault_cfg)
    assert layout.hot_md.read_bytes() == hot1
    assert layout.index_md.read_bytes() == index1
    assert {p.name: p.read_bytes() for p in layout.wiki_dir.glob("*.md")} == wiki1
    assert len(_log_entries(layout)) == entries1 + 1
