"""TDD tests for the sandbox workdir manager (tasks 3.015, 3.017, 3.018)."""

import stat
from pathlib import Path

import pytest

from archlens.sdk.sandbox import SandboxManager
from archlens.shared import files as files_mod
from archlens.shared.config import load_setup
from archlens.shared.errors import SandboxViolationError

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def sandbox(tmp_path: Path) -> SandboxManager:
    return SandboxManager(tmp_path / "runs")


def test_create_run_dir_is_isolated_per_run(sandbox: SandboxManager, tmp_path: Path):
    p1 = sandbox.create_run_dir("run1")
    p2 = sandbox.create_run_dir("run2")
    assert p1.is_dir() and p2.is_dir() and p1 != p2
    assert p1 == (tmp_path / "runs" / "run1").resolve()


def test_target_path_is_inside_run_dir_and_not_precreated(sandbox: SandboxManager):
    sandbox.create_run_dir("run1")
    target = sandbox.target_path("run1")
    assert target.parent == sandbox.create_run_dir("run1")
    assert target.name == "target"
    assert not target.exists()


def test_fresh_target_removes_a_leftover_clone_so_reruns_never_collide(sandbox: SandboxManager):
    sandbox.create_run_dir("run1")
    stale = sandbox.target_path("run1")
    stale.mkdir(parents=True)
    (stale / "leftover.py").write_text("old", encoding="utf-8")  # a prior clone
    fresh = sandbox.fresh_target("run1")
    assert fresh == stale and not fresh.exists()  # absent again -> git clone can proceed


def test_fresh_target_on_clean_run_is_a_noop(sandbox: SandboxManager):
    sandbox.create_run_dir("run1")
    assert not sandbox.fresh_target("run1").exists()


def test_force_rmtree_clears_readonly_pack_files(tmp_path: Path, monkeypatch):
    # Reproduces Windows: git marks pack files read-only and the first unlink raises;
    # the onexc handler must chmod +w and retry. Driven deterministically on any OS.
    victim = tmp_path / "pack.idx"
    victim.write_text("x", encoding="utf-8")
    victim.chmod(stat.S_IREAD)

    def fake_rmtree(path, onexc):
        onexc(Path.unlink, victim, PermissionError())

    monkeypatch.setattr(files_mod.shutil, "rmtree", fake_rmtree)
    files_mod.force_rmtree(tmp_path)
    assert not victim.exists()


def test_containment_rejects_paths_outside_root(sandbox: SandboxManager, tmp_path: Path):
    with pytest.raises(SandboxViolationError):
        sandbox.contain(tmp_path / "outside.txt")


def test_run_id_with_path_separators_rejected(sandbox: SandboxManager):
    with pytest.raises(SandboxViolationError):
        sandbox.create_run_dir("../evil")
    with pytest.raises(SandboxViolationError):
        sandbox.create_run_dir("a/b")


def test_cleanup_is_idempotent(sandbox: SandboxManager):
    run_dir = sandbox.create_run_dir("run1")
    (run_dir / "junk.txt").write_text("x", encoding="utf-8")
    sandbox.cleanup_run("run1")
    sandbox.cleanup_run("run1")  # double invocation must not raise
    assert not run_dir.exists()


def test_cleanup_stale_removes_only_unkept_runs(sandbox: SandboxManager):
    sandbox.create_run_dir("run1")
    sandbox.create_run_dir("run2")
    removed = sandbox.cleanup_stale(keep={"run1"})
    assert removed == ["run2"]
    assert sandbox.create_run_dir("run1").exists()


def test_configured_clone_path_is_outside_src_and_gitignored(setup_json):
    cfg = load_setup(setup_json)
    resolved = (PROJECT_ROOT / cfg.target_repo.workdir_root).resolve()
    assert not resolved.is_relative_to(PROJECT_ROOT / "src")
    gitignore = (PROJECT_ROOT / ".gitignore").read_text(encoding="utf-8")
    assert f"{cfg.target_repo.workdir_root}/" in gitignore
