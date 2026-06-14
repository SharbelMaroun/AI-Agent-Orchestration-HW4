"""Secrets policy: .env is git-ignored and .env-example holds only dummy values (task 13.045).

Expected: .gitignore ignores .env and the tracked .env-example contains no real-looking secrets.
"""

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_REAL_SECRET = re.compile(r"sk-ant-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}")


def test_env_is_git_ignored():
    """Expected: git check-ignore reports .env as ignored."""
    result = subprocess.run(["git", "check-ignore", ".env"],
                            cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0
    assert ".env" in result.stdout


def test_env_example_has_only_placeholder_values():
    """Expected: every .env-example value is a placeholder, with no real-looking secret."""
    example = ROOT / ".env-example"
    assert example.is_file()
    text = example.read_text(encoding="utf-8")
    assert not _REAL_SECRET.search(text)
    for line in text.splitlines():
        if "=" in line and not line.strip().startswith("#"):
            value = line.split("=", 1)[1].lower()
            assert "dummy" in value or "replace" in value or "example" in value
