"""Minimal .env loader (no dependency): populate os.environ from a .env file at startup.

Sets only non-empty keys that are not already present in the environment, so an explicitly exported
variable always wins and tests that pin the environment are never overridden.
"""

import os
from pathlib import Path


def load_dotenv(path: str | Path = ".env") -> None:
    """Load KEY=VALUE lines from a .env file into os.environ (non-empty, set-if-absent)."""
    file = Path(path)
    if not file.is_file():
        return
    for raw in file.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and value and key not in os.environ:
            os.environ[key] = value
