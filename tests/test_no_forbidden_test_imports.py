"""Meta-test: test modules import no real external-service clients (task 13.015).

Expected: tests/ contains no anthropic/openai/requests/httpx import; a seeded one fails the test.
"""

import re
from pathlib import Path

TESTS = Path(__file__).resolve().parent
_FORBIDDEN = re.compile(r"^\s*(?:import|from)\s+(anthropic|openai|requests|httpx)\b", re.MULTILINE)


def test_no_real_service_imports_in_tests():
    """Expected: zero forbidden real-service imports across all non-fixture test modules."""
    offenders = []
    for py_file in TESTS.rglob("*.py"):
        if "fixtures" in py_file.parts:
            continue
        if _FORBIDDEN.search(py_file.read_text(encoding="utf-8")):
            offenders.append(str(py_file.relative_to(TESTS)))
    assert offenders == [], f"forbidden service import in tests: {offenders}"
