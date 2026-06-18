"""GraphifyCLI — builds real `graphify` argv and executes via the gatekeeper (tasks 4.011-4.013).

Graphify's CLI has NO semantic edge-extraction command (the `/graphify` skill does that, not the
flow). Its only LLM step is `graphify label`, which names communities with the configured backend.
So the build is always the structural, no-LLM `graphify update`; when analysis_depth is semantic/full
we ADDITIONALLY run `graphify label` (configured backend; shipped default OpenAI gpt-4.1-mini) to
give communities readable names.
Graphify writes its artifacts (graph.json, graph.html, GRAPH_REPORT.md) to <repo>/graphify-out/.
The actual semantic reverse engineering is done by the ArchLens LLM agents over the graph, not here.
"""

from pathlib import Path

from ..graphops.config import GraphifyConfig


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
        """The structural build command. `update` = AST pass, no LLM (the only Graphify build cmd)."""
        return "update"

    def run(self, repo_path: Path) -> str:
        """Build the graph (`update`); when semantic, also label communities via the LLM backend."""
        output = self._gk.run_graphify(
            build_argv(self._cfg, self.command, repo_path), self.command, self._cfg.timeout_s)
        if self._cfg.semantic_enabled:
            label = [self._cfg.binary, "label", str(repo_path),
                     "--backend", self._cfg.llm_backend, "--model", self._cfg.llm_model]
            output += "\n" + self._gk.run_graphify(label, "label", self._cfg.timeout_s)
        return output
