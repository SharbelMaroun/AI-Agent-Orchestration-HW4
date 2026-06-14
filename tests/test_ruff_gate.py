"""Quality gate: ruff reports zero violations across src and tests (task 13.006).

Expected: `ruff check src tests` exits 0; a seeded violation would make it exit non-zero.
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _ruff_cmd() -> list[str]:
    found = shutil.which("ruff")
    return [found] if found else [sys.executable, "-m", "ruff"]


def test_ruff_clean_on_src_and_tests():
    """Expected: ruff check exits 0 over src and tests with no violations reported."""
    result = subprocess.run([*_ruff_cmd(), "check", "src", "tests"],
                            cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
