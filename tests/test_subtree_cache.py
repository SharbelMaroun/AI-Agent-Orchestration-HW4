"""TDD tests for subtree content-hash caching (tasks 4.040-4.041)."""

from pathlib import Path

from archlens.graphops.cache import SubtreeCache, subtree_hash


def _tree(root: Path) -> None:
    (root / "pkg").mkdir(parents=True)
    (root / "pkg" / "a.py").write_text("x = 1\n", encoding="utf-8")
    (root / "pkg" / "b.py").write_text("y = 2\n", encoding="utf-8")


def test_hash_stable_for_unchanged_tree(tmp_path: Path):
    _tree(tmp_path)
    assert subtree_hash(tmp_path) == subtree_hash(tmp_path)


def test_cache_miss_then_hit(tmp_path: Path):
    _tree(tmp_path)
    cache = SubtreeCache()
    assert cache.is_hit(tmp_path) is False
    cache.update(tmp_path)
    assert cache.is_hit(tmp_path) is True


def test_cache_miss_after_edit(tmp_path: Path):
    _tree(tmp_path)
    cache = SubtreeCache()
    cache.update(tmp_path)
    (tmp_path / "pkg" / "a.py").write_text("x = 999\n", encoding="utf-8")
    assert cache.is_hit(tmp_path) is False
