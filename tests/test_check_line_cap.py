"""Tests for the 150-line cap checker: blank/comment exclusion + tests in scope (task 16.001)."""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_line_cap.py"


def _load():
    spec = importlib.util.spec_from_file_location("check_line_cap_phase16", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_blank_and_comment_lines_excluded():
    mod = _load()
    assert mod.effective_lines("# comment\n\n  x = 1  \n   # indented\ny = 2\n") == 2


def test_tests_directory_is_in_default_scope():
    assert "tests" in _load().DEFAULT_ROOTS


def test_over_cap_file_flagged(tmp_path):
    mod = _load()
    (tmp_path / "big.py").write_text("\n".join(f"v{i} = {i}" for i in range(151)), encoding="utf-8")
    assert mod.scan([tmp_path])
