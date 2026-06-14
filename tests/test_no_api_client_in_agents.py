"""Guard: no agent module imports an external API/HTTP client (task 11.017).

All RefactorAgent LLM fix-generation calls must route through gatekeeper/gatekeeper.py;
only the gatekeeper package may import an API client.
"""

import re
from pathlib import Path

AGENTS = Path(__file__).resolve().parents[1] / "src" / "archlens" / "agents"
_FORBIDDEN = re.compile(r"\b(anthropic|openai|httpx|requests)\b")


def test_agents_import_no_api_client():
    offenders = []
    for py_file in AGENTS.rglob("*.py"):
        for line in py_file.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith(("import ", "from ")) and _FORBIDDEN.search(stripped):
                offenders.append(f"{py_file.name}: {stripped}")
    assert offenders == [], f"agents import an API client (must route via gatekeeper): {offenders}"
