"""Guard: the LLM client library is imported only inside the gatekeeper (task 12.010)."""

import re
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "archlens"
_IMPORT = re.compile(r"^\s*(import anthropic|from anthropic)", re.MULTILINE)


def test_anthropic_imported_only_in_gatekeeper():
    offenders = []
    for py_file in SRC.rglob("*.py"):
        if "gatekeeper" in py_file.parts:
            continue
        if _IMPORT.search(py_file.read_text(encoding="utf-8")):
            offenders.append(str(py_file.relative_to(SRC)))
    assert offenders == [], f"anthropic imported outside gatekeeper: {offenders}"
