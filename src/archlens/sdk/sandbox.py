"""Sandbox workdir manager — per-run isolated directories with strict containment."""

import os
import shutil
import stat
from pathlib import Path

from ..shared.errors import SandboxViolationError


def _force_rmtree(path: Path) -> None:
    """rmtree that clears read-only bits (Windows marks git pack files read-only) and retries."""
    def _clear_readonly(func, target, _exc):
        os.chmod(target, stat.S_IWRITE)
        func(target)

    shutil.rmtree(path, onexc=_clear_readonly)


class SandboxManager:
    """Creates, contains, and cleans per-run working directories under one root."""

    def __init__(self, workdir_root: str | Path) -> None:
        self._root = Path(workdir_root).resolve()

    @property
    def root(self) -> Path:
        return self._root

    def _check_run_id(self, run_id: str) -> str:
        if not run_id or any(sep in run_id for sep in ("/", "\\", "..")):
            raise SandboxViolationError(f"malformed run id: {run_id!r}")
        return run_id

    def contain(self, path: str | Path) -> Path:
        resolved = Path(path).resolve()
        if not resolved.is_relative_to(self._root):
            raise SandboxViolationError(f"path escapes sandbox root {self._root}: {resolved}")
        return resolved

    def create_run_dir(self, run_id: str) -> Path:
        run_dir = self.contain(self._root / self._check_run_id(run_id))
        run_dir.mkdir(parents=True, exist_ok=True)
        return run_dir

    def target_path(self, run_id: str) -> Path:
        """Clone destination inside the run dir; intentionally NOT pre-created (git clone needs it absent)."""
        return self.contain(self._root / self._check_run_id(run_id) / "target")

    def fresh_target(self, run_id: str) -> Path:
        """Absent clone destination: remove any leftover clone so a re-run never collides."""
        target = self.target_path(run_id)
        if target.exists():
            _force_rmtree(target)
        return target

    def cleanup_run(self, run_id: str) -> None:
        """Idempotent: removing a missing run dir is a no-op, never an error."""
        run_dir = self.contain(self._root / self._check_run_id(run_id))
        if run_dir.exists():
            _force_rmtree(run_dir)

    def cleanup_stale(self, keep: set[str]) -> list[str]:
        """Remove every run dir whose name is not in `keep`; return removed names sorted."""
        removed = []
        if not self._root.exists():
            return removed
        for child in sorted(self._root.iterdir()):
            if child.is_dir() and child.name not in keep:
                _force_rmtree(self.contain(child))
                removed.append(child.name)
        return removed
