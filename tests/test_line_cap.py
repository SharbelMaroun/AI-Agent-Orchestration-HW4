"""TDD tests for the 150 effective-line cap checker (task 1.039)."""

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_line_cap.py"


def _load_checker():
    spec = importlib.util.spec_from_file_location("check_line_cap", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_blank_and_comment_lines_excluded():
    mod = _load_checker()
    text = "\n".join(["# comment", "", "x = 1", "   # indented comment", "y = 2", ""])
    assert mod.effective_lines(text) == 2


def test_150_effective_lines_pass(tmp_path: Path):
    mod = _load_checker()
    body = ["# header comment", ""] + [f"v{i} = {i}" for i in range(150)]
    (tmp_path / "ok.py").write_text("\n".join(body), encoding="utf-8")
    assert mod.scan([tmp_path]) == []


def test_151_effective_lines_fail(tmp_path: Path):
    mod = _load_checker()
    (tmp_path / "bad.py").write_text(
        "\n".join(f"v{i} = {i}" for i in range(151)), encoding="utf-8"
    )
    over = mod.scan([tmp_path])
    assert [(p.name, n) for p, n in over] == [("bad.py", 151)]


def test_real_src_and_tests_within_cap():
    mod = _load_checker()
    root = Path(__file__).resolve().parents[1]
    assert mod.scan([root / "src", root / "tests"]) == []
