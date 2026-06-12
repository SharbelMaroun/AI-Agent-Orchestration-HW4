"""ArchLensSDK — the single entry point for all business logic.

GUI/CLI layers hold zero logic; they call this facade exclusively.
"""

from pathlib import Path

from archlens.sdk.repo_config import select_repo
from archlens.sdk.sandbox import SandboxManager
from archlens.sdk.validation import ValidationResult, validate_repo
from archlens.shared.config import SetupConfig, load_setup
from archlens.shared.version import get_version


class ArchLensSDK:
    """Facade over all ArchLens capabilities (grows phase by phase)."""

    def __init__(self, setup: SetupConfig | None = None, gatekeeper=None) -> None:
        self._setup = setup
        self._gatekeeper = gatekeeper

    def _config(self) -> SetupConfig:
        if self._setup is None:
            self._setup = load_setup()
        return self._setup

    def _gk(self):
        if self._gatekeeper is None:
            from archlens.gatekeeper.gatekeeper import Gatekeeper

            self._gatekeeper = Gatekeeper()
        return self._gatekeeper

    def version(self) -> str:
        return get_version()

    def clone_target_repo(self, run_id: str, use_fallback: bool = False) -> Path:
        """Clone the configured repo into a sandboxed per-run directory via the gatekeeper."""
        repo = select_repo(self._config(), use_fallback)
        sandbox = SandboxManager(repo.workdir_root)
        sandbox.create_run_dir(run_id)
        return self._gk().git_clone(repo, sandbox.target_path(run_id))

    def validate_repo(self, repo_dir: Path, use_fallback: bool = False) -> ValidationResult:
        """Run the four validation checks against a cloned checkout."""
        cfg = self._config()
        repo = select_repo(cfg, use_fallback)
        return validate_repo(repo_dir, cfg.validation, repo.max_size_mb)
