"""Unchanged-subtree cache keys so the extract stage can be skipped on hits (tasks 4.040-4.041)."""

import hashlib
from pathlib import Path


def subtree_hash(root) -> str:
    """Content hash of a directory tree: sorted (relpath, sha256(file)) pairs."""
    root = Path(root)
    parts = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        parts.append(f"{rel}:{digest}")
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


class SubtreeCache:
    """Remembers subtree hashes; is_hit() is true only when nothing changed."""

    def __init__(self) -> None:
        self._seen: dict[str, str] = {}

    def is_hit(self, root) -> bool:
        return self._seen.get(str(Path(root))) == subtree_hash(root)

    def update(self, root) -> None:
        self._seen[str(Path(root))] = subtree_hash(root)
