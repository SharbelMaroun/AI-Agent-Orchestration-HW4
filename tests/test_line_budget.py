"""Repo-wide 150-effective-line audit, run in the default suite (task 8.045)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _effective_lines(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip() and not line.strip().startswith("#"))


def test_no_source_or_test_file_exceeds_150_effective_lines():
    offenders = []
    for subdir in ("src", "tests"):
        for py_file in (ROOT / subdir).rglob("*.py"):
            if "fixtures" in py_file.parts:  # test data (e.g. planted oversized modules) is exempt
                continue
            count = _effective_lines(py_file.read_text(encoding="utf-8"))
            if count > 150:
                offenders.append(f"{py_file.relative_to(ROOT)}: {count}")
    assert offenders == [], f"files over 150 effective lines: {offenders}"
