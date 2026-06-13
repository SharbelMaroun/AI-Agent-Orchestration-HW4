"""GraphifyCLI — builds real `graphify` argv and executes via the gatekeeper (tasks 4.011-4.013).

Structural runs use `graphify update` (AST only, no LLM); semantic runs use `graphify extract`.
Graphify writes its artifacts (graph.json, graph.html, GRAPH_REPORT.md) to <repo>/graphify-out/.
"""

from pathlib import Path

from archlens.graphops.config import GraphifyConfig


def build_argv(cfg: GraphifyConfig, command: str, repo_path: Path) -> list[str]:
    """Construct the argv for a Graphify command, e.g. `graphify update <repo>`."""
    return [cfg.binary, command, str(repo_path)]


class GraphifyCLI:
    """Thin builder/executor; all process spawning is delegated to the gatekeeper."""

    def __init__(self, cfg: GraphifyConfig, gatekeeper) -> None:
        self._cfg = cfg
        self._gk = gatekeeper

    @property
    def command(self) -> str:
        """`update` = structural AST pass (no LLM); `extract` = semantic pass."""
        return "extract" if self._cfg.semantic_enabled else "update"

    def run(self, repo_path: Path) -> str:
        argv = build_argv(self._cfg, self.command, repo_path)
        return self._gk.run_graphify(argv, self.command, self._cfg.timeout_s)
