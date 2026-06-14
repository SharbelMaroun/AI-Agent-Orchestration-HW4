"""TDD tests for RefactorFixes.merge_duplicates (task 11.022)."""

from pathlib import Path

import pytest

from archlens.agents.refactor_fixes import RefactorFixes

_FUNC = "def shared_logic(x):\n    return x * 2 + 1\n"


def _pair(tmp_path: Path, level: str = "VALIDATED", similarity: float = 0.95) -> dict:
    a = tmp_path / "a.py"
    b = tmp_path / "b.py"
    a.write_text(_FUNC, encoding="utf-8")
    b.write_text(_FUNC, encoding="utf-8")
    return {"level": level, "similarity": similarity,
            "func_name": "shared_logic", "sources": [str(a), str(b)]}


def test_merge_relocates_to_shared_module(tmp_path):
    shared = RefactorFixes().merge_duplicates(_pair(tmp_path), tmp_path / "shared.py")
    assert "def shared_logic" in shared.read_text(encoding="utf-8")


def test_merge_updates_both_call_sites(tmp_path):
    pair = _pair(tmp_path)
    RefactorFixes().merge_duplicates(pair, tmp_path / "shared.py")
    for source in pair["sources"]:
        text = Path(source).read_text(encoding="utf-8")
        assert "from shared import shared_logic" in text
        assert "def shared_logic" not in text


def test_merge_refuses_low_similarity(tmp_path):
    with pytest.raises(ValueError):
        RefactorFixes().merge_duplicates(_pair(tmp_path, similarity=0.80), tmp_path / "shared.py")


def test_merge_refuses_unvalidated_level(tmp_path):
    with pytest.raises(ValueError):
        RefactorFixes().merge_duplicates(_pair(tmp_path, level="EXTRACTED"), tmp_path / "shared.py")
