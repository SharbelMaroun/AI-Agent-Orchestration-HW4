"""Guard: only the gatekeeper package imports an API/HTTP client (task 9.047)."""

import re
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "archlens"
_FORBIDDEN = re.compile(r"\b(anthropic|openai|httpx|requests)\b")


def test_no_api_client_imports_outside_gatekeeper():
    offenders = []
    for py_file in SRC.rglob("*.py"):
        if "gatekeeper" in py_file.parts:
            continue
        for line in py_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith(("import ", "from ")) and _FORBIDDEN.search(stripped):
                offenders.append(f"{py_file.name}: {stripped}")
    assert offenders == [], f"API client imported outside gatekeeper: {offenders}"
