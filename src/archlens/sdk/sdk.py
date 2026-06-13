"""ArchLensSDK — the single entry point for all business logic.

GUI/CLI layers hold zero logic; they call this facade exclusively.
"""

from pathlib import Path

from archlens.graphops.cli_wrapper import GraphifyCLI
from archlens.graphops.diff import GraphDiff, compute_diff
from archlens.graphops.layout import RunLayout, new_run_id
from archlens.graphops.manifest import Manifest, save_manifest
from archlens.graphops.orchestrator import run_pipeline
from archlens.graphops.parser import Graph, parse_graph
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

    def run_graphify_pipeline(self, repo_path: Path, run_id: str | None = None) -> Manifest:
        """Run the five-stage Graphify pipeline (via the gatekeeper) and persist a run manifest."""
        cfg = self._config().graphify
        rid = run_id or new_run_id()
        layout = RunLayout(Path(cfg.output_root), rid)
        results = run_pipeline(GraphifyCLI(cfg, self._gk()), repo_path)
        manifest = Manifest(run_id=rid, analysis_depth=cfg.analysis_depth, stages=results)
        save_manifest(layout, manifest)
        return manifest

    def parse_graph(self, source) -> Graph:
        """Validate and load a graph.json into the Graph aggregate."""
        return parse_graph(source)

    def diff_graphs(self, before, after, bottleneck: str | None = None) -> GraphDiff:
        """Diff two Graphify runs for the improvement-loop stop conditions."""
        return compute_diff(parse_graph(before), parse_graph(after), bottleneck)
