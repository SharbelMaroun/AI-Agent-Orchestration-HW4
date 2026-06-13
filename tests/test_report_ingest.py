"""TDD tests for REPORT.md ingestion (tasks 4.036-4.037)."""

from pathlib import Path

from archlens.graphops.report import ReportSummary, ingest_report

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "graphify"


def test_ingest_extracts_sections_and_metrics():
    summary = ingest_report(FIXTURES / "REPORT.md")
    assert summary.sections == ["Graph Report", "Summary", "Findings"]
    assert summary.metrics["nodes"] == "6"
    assert "Metric" not in summary.metrics


def test_report_summary_json_round_trip():
    summary = ingest_report(FIXTURES / "REPORT.md")
    restored = ReportSummary.model_validate_json(summary.model_dump_json())
    assert restored == summary
