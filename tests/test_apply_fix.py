"""Tests for sdk.apply_fix — really splits a target module, no-op on a missing file."""

from archlens.sdk.sdk import ArchLensSDK


def test_apply_fix_splits_a_real_module_and_reports_success(tmp_path):
    module = tmp_path / "god.py"
    module.write_text("def a():\n    return 1\n\n\ndef b():\n    return 2\n", encoding="utf-8")
    ok = ArchLensSDK().apply_fix({"source_file": "god.py", "category": "god_node"}, str(tmp_path))
    assert ok is True
    assert (tmp_path / "god_part1.py").is_file()              # a part was emitted
    assert "import *" in module.read_text(encoding="utf-8")   # original is now a facade


def test_apply_fix_is_a_safe_noop_when_the_file_is_missing(tmp_path):
    assert ArchLensSDK().apply_fix({"source_file": "nope.py"}, str(tmp_path)) is False
