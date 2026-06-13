"""TDD tests for the append-only log.md journal (tasks 5.027-5.028)."""

from datetime import datetime, timezone
from pathlib import Path

from archlens.vault.log_journal import append_entry


def test_entries_are_appended_not_truncated(tmp_path: Path):
    log = tmp_path / "log.md"
    append_entry(log, "run", "graph.json", when=datetime(2026, 6, 13, tzinfo=timezone.utc))
    append_entry(log, "vault-build", "vault", when=datetime(2026, 6, 13, 1, tzinfo=timezone.utc))
    text = log.read_text(encoding="utf-8")
    entries = [ln for ln in text.splitlines() if ln.startswith("- ")]
    assert len(entries) == 2
    assert text.startswith("# Ingestion Log")
    assert "graph.json" in text


def test_iso8601_timestamp(tmp_path: Path):
    log = tmp_path / "log.md"
    line = append_entry(log, "run", "x", when=datetime(2026, 6, 13, 12, 30, tzinfo=timezone.utc))
    assert "2026-06-13T12:30:00+00:00" in line
