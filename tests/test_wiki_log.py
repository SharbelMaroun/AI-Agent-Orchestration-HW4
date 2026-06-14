"""TDD tests for the log.md wiki-build journal (task 14.027)."""

from archlens.vault.wiki_log import append_log


def test_entry_has_timestamp_source_action_outcome(tmp_path):
    log = tmp_path / "log.md"
    line = append_log(log, "raw", "ingest", "ok")
    parts = [p.strip() for p in line.lstrip("- ").split("|")]
    assert len(parts) == 4
    assert parts[1:] == ["raw", "ingest", "ok"]


def test_append_only_preserves_order(tmp_path):
    log = tmp_path / "log.md"
    append_log(log, "raw", "ingest", "ok")
    append_log(log, "wiki", "build", "3 pages")
    append_log(log, "index", "build", "2 topics")
    body = log.read_text(encoding="utf-8")
    assert body.index("ingest") < body.index("wiki | build") < body.index("index | build")
