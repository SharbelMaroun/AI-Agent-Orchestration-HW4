"""ArchLensSDK — the single entry point for all business logic.

GUI/CLI layers hold zero logic; they call this facade exclusively. Phase-specific method
groups live in mixins (analysis_mixin, deliverables_mixin) to honour the 150-line file cap.
"""

from pathlib import Path

from ..graphops.adapter import load_graphify_graph
from ..graphops.cli_wrapper import GraphifyCLI
from ..graphops.diff import GraphDiff, compute_diff
from ..graphops.layout import RunLayout, new_run_id
from ..graphops.manifest import Manifest, save_manifest
from ..graphops.orchestrator import run_pipeline
from ..graphops.parser import Graph, parse_graph
from ..sdk.analysis_mixin import GraphAnalysisMixin
from ..sdk.debug_mixin import DebugDemoMixin
from ..sdk.deliverables_mixin import DeliverablesMixin
from ..sdk.knowledge_mixin import KnowledgeMixin
from ..sdk.llm_mixin import LLMMixin
from ..sdk.metrics_mixin import MetricsMixin
from ..sdk.orchestration_mixin import OrchestrationMixin
from ..sdk.plugins import PluginRegistry
from ..sdk.refactor_mixin import RefactorMixin
from ..sdk.repo_config import select_repo
from ..sdk.research_mixin import ResearchMixin
from ..sdk.sandbox import SandboxManager
from ..sdk.validation import ValidationResult, validate_repo
from ..shared.config import SetupConfig, load_setup
from ..shared.dotenv import load_dotenv
from ..shared.version import get_version
from ..vault.builder import build_vault as _build_vault
from ..vault.layout import VaultLayout
from ..vault.raw_ingest import default_graph_raw_sources


class ArchLensSDK(GraphAnalysisMixin, DeliverablesMixin, DebugDemoMixin, OrchestrationMixin, MetricsMixin,
                  KnowledgeMixin, ResearchMixin, LLMMixin, RefactorMixin):
    """Facade over all ArchLens capabilities; phase method groups are added via mixins."""

    def __init__(self, setup: SetupConfig | None = None, gatekeeper=None) -> None:
        load_dotenv()  # read .env so a pasted API key enables live LLM mode automatically
        self._setup = setup
        self._gatekeeper = gatekeeper
        self._plugin_registry: PluginRegistry | None = None

    def _config(self) -> SetupConfig:
        if self._setup is None:
            self._setup = load_setup()
        return self._setup

    def _gk(self):
        if self._gatekeeper is None:
            from ..gatekeeper.gatekeeper import Gatekeeper

            self._gatekeeper = Gatekeeper()
        return self._gatekeeper

    def version(self) -> str:
        """Return the ArchLens version string."""
        return get_version()

    def agent_plugins(self) -> PluginRegistry:
        """The agent-plugin extension registry (allowlist from config.sdk.plugin_allowlist).

        Owned by the SDK so the AgentPlugin extension point is a first-class production seam, not
        only exercised by tests. Registered plugins are the documented way to add agents.
        """
        if self._plugin_registry is None:
            self._plugin_registry = PluginRegistry(self._config().sdk.plugin_allowlist)
        return self._plugin_registry

    def register_agent_plugin(self, name: str, plugin: object) -> bool:
        """Register an agent plugin through the SDK; honors the configured allowlist."""
        return self.agent_plugins().register_agent_plugin(name, plugin)

    def clone_target_repo(self, run_id: str, use_fallback: bool = False) -> Path:
        """Clone the configured repo into a sandboxed per-run directory via the gatekeeper."""
        repo = select_repo(self._config(), use_fallback)
        sandbox = SandboxManager(repo.workdir_root)
        sandbox.create_run_dir(run_id)
        return self._gk().git_clone(repo, sandbox.fresh_target(run_id))

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

    def build_vault(self, graph_source, raw_sources: list | None = None) -> VaultLayout:
        """Build the Obsidian vault (hot.md, index.md, wiki/, log.md, raw/) from a graph.json.

        Accepts a real Graphify graph.json (node-link) or our canonical schema via the adapter.
        """
        is_graph = isinstance(graph_source, Graph)
        graph = graph_source if is_graph else load_graphify_graph(graph_source)
        if raw_sources is None and not is_graph:
            raw_sources = default_graph_raw_sources(graph_source)
        return _build_vault(graph, self._config().vault, raw_sources)

    def validate_config(self, setup_path: str = "config/setup.json",
                        rate_limits_path: str = "config/rate_limits.json",
                        env_example: str = ".env-example") -> bool:
        """Validate the config files; raise ConfigError naming the offending file on any error."""
        from ..shared.exceptions import ConfigError
        from ..shared.rate_limits import load_rate_limits

        try:
            load_setup(setup_path)
        except Exception as exc:
            raise ConfigError(f"setup.json: {exc}", source_context="config/setup.json") from exc
        try:
            load_rate_limits(rate_limits_path)
        except Exception as exc:
            raise ConfigError(f"rate_limits.json: {exc}", source_context="config/rate_limits.json") from exc
        if not Path(env_example).is_file():
            raise ConfigError(".env-example missing", source_context=".env-example")
        return True

    def token_usage(self) -> dict:
        """Real token usage the gatekeeper recorded this session (per-call input/output tokens)."""
        ledger = self._gk().usage_ledger
        rows = [{"agent": e.agent, "model": e.model,
                 "input_tokens": e.input_tokens, "output_tokens": e.output_tokens}
                for e in ledger.entries]
        total = ledger.total_tokens()
        return {"baseline": 0, "assisted": total, "total": total,
                "input": ledger.total_input(), "output": ledger.total_output(), "rows": rows}
