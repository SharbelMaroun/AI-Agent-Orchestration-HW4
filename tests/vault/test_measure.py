"""TDD tests for the before/after knowledge-asset measurement table (task 5.047)."""

from pathlib import Path

from archlens.vault.measure import append_measurements, knowledge_asset_metrics, render_measurements


def test_four_metrics_each_with_before_and_after(vault_graph, vault_cfg):
    metrics = knowledge_asset_metrics(vault_graph, vault_cfg)
    assert len(metrics) == 4
    for before, after in metrics.values():
        assert before is not None and after is not None


def test_render_has_four_data_rows(vault_graph, vault_cfg):
    table = render_measurements(knowledge_asset_metrics(vault_graph, vault_cfg))
    data_rows = [ln for ln in table.splitlines() if ln.startswith("| ") and "Metric" not in ln]
    assert len(data_rows) == 4
    assert "source_traceability" in table


def test_append_writes_table_to_log(vault_graph, vault_cfg, tmp_path: Path):
    log = tmp_path / "log.md"
    log.write_text("# Ingestion Log\n", encoding="utf-8")
    append_measurements(log, knowledge_asset_metrics(vault_graph, vault_cfg))
    text = log.read_text(encoding="utf-8")
    assert text.startswith("# Ingestion Log")  # not truncated
    assert "Knowledge-asset measurement" in text
    assert "| Metric | Before | After |" in text
