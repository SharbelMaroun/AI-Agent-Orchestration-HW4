"""TDD test for the thin `deliverables` CLI subcommand (task 7.042)."""

from pathlib import Path

from archlens.__main__ import main

FIX = Path(__file__).resolve().parent / "fixtures"
PRD = FIX / "prd_sample.md"
FULL = FIX / "graphify" / "full.json"
CLASSES = FIX / "classes_pkg"


def test_deliverables_command_writes_three_files(tmp_path):
    code = main([
        "deliverables",
        "--graph", str(FULL),
        "--src", str(CLASSES),
        "--prd", str(PRD),
        "--out", str(tmp_path),
    ])
    assert code == 0
    for name in ("ARCHITECTURE.md", "CLASS_SCHEMA.md", "ALIGNMENT_AUDIT.md"):
        assert (tmp_path / name).is_file()
