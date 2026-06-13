"""log.md ingestion journal — append-only, ISO-8601 timestamped entries (tasks 5.027-5.028)."""

from datetime import datetime, timezone
from pathlib import Path

_HEADER = "# Ingestion Log\n\n"


def append_entry(log_path, action: str, source: str, when: datetime | None = None) -> str:
    """Append one journal line; existing content is never truncated."""
    stamp = (when or datetime.now(timezone.utc)).isoformat()
    line = f"- {stamp} | {action} | {source}\n"
    path = Path(log_path)
    existing = path.read_text(encoding="utf-8") if path.exists() else _HEADER
    path.write_text(existing + line, encoding="utf-8")
    return line
