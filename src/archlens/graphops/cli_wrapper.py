"""GraphifyCLI — builds per-stage 'uv run' argv and executes via the gatekeeper (tasks 4.011-4.013)."""

from pathlib import Path

from archlens.graphops.config import GraphifyConfig


def build_argv(cfg: GraphifyConfig, stage: str, repo_path: Path) -> list[str]:
    """Construct the exact argv for one stage (Graphify is invoked only via 'uv run')."""
    return [
        "uv",
        "run",
        cfg.binary,
        "--stage",
        stage,
        "--repo",
        str(repo_path),
        "--depth",
        cfg.analysis_depth,
    ]


class GraphifyCLI:
    """Thin builder/executor; all process spawning is delegated to the gatekeeper."""

    def __init__(self, cfg: GraphifyConfig, gatekeeper) -> None:
        self._cfg = cfg
        self._gk = gatekeeper

    def run_stage(self, stage: str, repo_path: Path) -> str:
        argv = build_argv(self._cfg, stage, repo_path)
        return self._gk.run_graphify_stage(argv, stage, self._cfg.timeout_s)
