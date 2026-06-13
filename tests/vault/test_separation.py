"""TDD test: raw/ vs wiki/ separation (task 5.031)."""

from pathlib import Path

from archlens.vault.builder import build_vault

GRAPHIFY = Path(__file__).resolve().parents[1] / "fixtures" / "graphify"


def test_wiki_notes_never_link_into_raw(vault_graph, vault_cfg):
    layout = build_vault(
        vault_graph, vault_cfg, raw_sources=[GRAPHIFY / "full.json", GRAPHIFY / "REPORT.md"]
    )
    for note in layout.wiki_dir.glob("*.md"):
        assert "raw/" not in note.read_text(encoding="utf-8")
    raw_names = {p.name for p in layout.raw_dir.iterdir()}
    assert "hot.md" not in raw_names
    assert "index.md" not in raw_names
