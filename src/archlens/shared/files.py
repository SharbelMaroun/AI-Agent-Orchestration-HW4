"""Filesystem helpers shared across ArchLens modules."""

import os
import shutil
import stat
from pathlib import Path


def force_rmtree(path: Path) -> None:
    """Remove a tree, clearing read-only bits first on Windows git pack files."""
    def _clear_readonly(func, target, _exc):
        os.chmod(target, stat.S_IWRITE)
        func(target)

    shutil.rmtree(path, onexc=_clear_readonly)
