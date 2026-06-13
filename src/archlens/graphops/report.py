"""REPORT.md ingestion into structured ReportSummary records (tasks 4.036-4.037)."""

import re
from pathlib import Path

from pydantic import BaseModel, ConfigDict

_HEADING = re.compile(r"^#{1,6}\s+(.*)$")
_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$")


class ReportSummary(BaseModel):
    """Headings and 2-column metric tables extracted from a Graphify REPORT.md."""

    model_config = ConfigDict(extra="forbid")

    sections: list[str] = []
    metrics: dict[str, str] = {}


def ingest_report(source: str | Path) -> ReportSummary:
    """Parse REPORT.md headings and 2-column metric tables into a ReportSummary."""
    text = Path(source).read_text(encoding="utf-8")
    sections: list[str] = []
    metrics: dict[str, str] = {}
    for line in text.splitlines():
        heading = _HEADING.match(line)
        if heading:
            sections.append(heading.group(1).strip())
            continue
        row = _ROW.match(line)
        if row:
            key, value = row.group(1).strip(), row.group(2).strip()
            if key.lower() != "metric" and set(value) != {"-"}:
                metrics[key] = value
    return ReportSummary(sections=sections, metrics=metrics)
