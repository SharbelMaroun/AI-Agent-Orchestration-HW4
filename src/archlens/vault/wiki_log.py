"""log.md journal for the LLM-wiki pipeline — append-only, with an outcome field (task 14.028)."""

from datetime import datetime, timezone
from pathlib import Path

_HEADER = "# Wiki Build Log\n\n"


def append_log(log_path, source: str, action: str, outcome: str,
               when: datetime | None = None) -> str:
    """Append one journal line (timestamp | source | action | outcome); never truncates."""
    stamp = (when or datetime.now(timezone.utc)).isoformat()
    line = f"- {stamp} | {source} | {action} | {outcome}\n"
    path = Path(log_path)
    existing = path.read_text(encoding="utf-8") if path.exists() else _HEADER
    path.write_text(existing + line, encoding="utf-8")
    return line
