"""Debug gate: the FIXED andela/buggy-python harness passes (failing->passing proof, EX04 §5.4).

Skips when the git-ignored clone is absent (CI / fresh checkout) — the committed proof of the fix is
``deliverables/BUG_REPORT.md`` (symptom, root cause, diff, transcript). Locally, after cloning the
repo into ``runs/buggy-python`` and applying the documented fix, this runs the repo's OWN ``main.py``
harness as a subprocess and asserts it reaches the success line at exit 0.
"""

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2] / "runs" / "buggy-python"


@pytest.mark.skipif(
    not (REPO / "main.py").is_file(),
    reason="buggy-python clone absent (git-ignored runs/); see deliverables/BUG_REPORT.md to reproduce",
)
def test_fixed_buggy_python_harness_passes():
    """Expected: the fixed buggy-python harness prints the success line at exit 0."""
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    proc = subprocess.run([sys.executable, "main.py"], cwd=REPO, capture_output=True, env=env)
    out = proc.stdout.decode("utf-8", "replace") + proc.stderr.decode("utf-8", "replace")
    assert proc.returncode == 0, out
    assert "All test passed successfully" in out
