"""TDD tests for raw/ ingestion with checksums (tasks 5.029-5.031)."""

import hashlib
from pathlib import Path

from archlens.vault.layout import VaultLayout
from archlens.vault.raw_ingest import ingest_raw

GRAPHIFY = Path(__file__).resolve().parents[1] / "fixtures" / "graphify"


def test_raw_copies_are_byte_identical_and_logged(vault_cfg):
    layout = VaultLayout(vault_cfg)
    digests = ingest_raw(layout, [GRAPHIFY / "full.json", GRAPHIFY / "REPORT.md"])
    for name in ("full.json", "REPORT.md"):
        src, dest = GRAPHIFY / name, layout.raw_dir / name
        assert dest.read_bytes() == src.read_bytes()
        assert digests[name] == hashlib.sha256(src.read_bytes()).hexdigest()
    assert "raw-ingest" in layout.log_md.read_text(encoding="utf-8")


def test_no_wiki_page_writes_into_raw(vault_cfg):
    layout = VaultLayout(vault_cfg)
    ingest_raw(layout, [GRAPHIFY / "full.json"])
    assert layout.raw_dir.is_dir()
    assert not any(p.suffix == ".md" and "wiki" in str(p) for p in layout.raw_dir.iterdir())
