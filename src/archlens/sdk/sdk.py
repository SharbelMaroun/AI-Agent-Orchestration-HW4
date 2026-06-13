"""ArchLensSDK — the single entry point for all business logic.

GUI/CLI layers hold zero logic; they call this facade exclusively.
"""

from pathlib import Path

from archlens.graphops import commands as _commands
from archlens.graphops.adapter import load_graphify_graph
from archlens.graphops.block_model import build_block_model
from archlens.graphops.bridges import bridge_report
from archlens.graphops.centrality import degree_centrality
from archlens.graphops.classify import classify
from archlens.graphops.cli_wrapper import GraphifyCLI
from archlens.graphops.communities import community_folder_mismatches, detect_communities
from archlens.graphops.diff import GraphDiff, compute_diff
from archlens.graphops.duplicates import route_duplicates_to_review
from archlens.graphops.graph_metrics import modularity
from archlens.graphops.layout import RunLayout, new_run_id
from archlens.graphops.loader import load_graph
from archlens.graphops.manifest import Manifest, save_manifest
from archlens.graphops.mermaid_blocks import render_block_diagram
from archlens.graphops.orchestrator import run_pipeline
from archlens.graphops.parser import Graph, parse_graph
from archlens.graphops.spof import critical_paths, spof_detect
from archlens.graphops.triage import triage_edges
from archlens.graphops.views import macro_view, meso_view, micro_view
from archlens.sdk.repo_config import select_repo
from archlens.sdk.sandbox import SandboxManager
from archlens.sdk.validation import ValidationResult, validate_repo
from archlens.shared.config import SetupConfig, load_setup
from archlens.shared.version import get_version
from archlens.vault.builder import build_vault as _build_vault
from archlens.vault.layout import VaultLayout


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

    def build_vault(self, graph_source, raw_sources: list | None = None) -> VaultLayout:
        """Build the Obsidian vault (hot.md, index.md, wiki/, log.md, raw/) from a graph.json.

        Accepts a real Graphify graph.json (node-link) or our canonical schema via the adapter.
        """
        graph = graph_source if isinstance(graph_source, Graph) else load_graphify_graph(graph_source)
        return _build_vault(graph, self._config().vault, raw_sources)

    # --- Phase 6 graph-analysis facade (delegates to graphops; callers never import it) ---

    def load_analysis_graph(self, source):
        """Load a graph.json into a networkx DiGraph for analysis."""
        return load_graph(source)

    def node_centrality(self, graph):
        """Ranked degree and betweenness centrality rows."""
        return degree_centrality(graph)

    def classify_nodes(self, graph):
        """Label nodes HUB or BOTTLENECK with a rationale."""
        return classify(graph)

    def density_communities(self, graph):
        """Detect density-based communities (never folder-based)."""
        return detect_communities(graph)

    def folder_mismatches(self, graph, communities):
        """Nodes whose community disagrees with their source folder."""
        return community_folder_mismatches(graph, communities)

    def modularity_score(self, graph, communities):
        """Partition modularity over the undirected projection."""
        return modularity(graph, communities)

    def bridge_report(self, graph, communities):
        """Structural bridges and community connectors, kept separate."""
        return bridge_report(graph, communities)

    def critical_paths(self, graph):
        """Paths composed entirely of critical-relation edges."""
        return critical_paths(graph)

    def single_points_of_failure(self, graph):
        """Nodes on every critical path, each with its citation chain."""
        return spof_detect(graph)

    def triage_edges(self, graph):
        """Bucket edges by evidence type (EXTRACTED/INFERRED/AMBIGUOUS)."""
        return triage_edges(graph)

    def duplicate_review_queue(self, graph):
        """Route duplicate findings into the human-review queue (never merges)."""
        return route_duplicates_to_review(graph)

    def macro_view(self, graph):
        """Whole-graph summary (counts, density, components, top hubs)."""
        return macro_view(graph)

    def meso_view(self, graph, communities):
        """Per-community summaries including their connector edges."""
        return meso_view(graph, communities)

    def micro_view(self, graph, node):
        """Single-node neighbourhood with cited edges."""
        return micro_view(graph, node)

    def query_graph(self, graph, node=None, edge=None):
        """Filter nodes and edges by attribute."""
        return _commands.query(graph, node, edge)

    def shortest_path(self, graph, src, dst):
        """Shortest path from src to dst as a per-hop citation chain."""
        return _commands.path(graph, src, dst)

    def explain_edge(self, graph, src, dst):
        """Explain why an edge exists (relation, confidence, source_file)."""
        return _commands.explain(graph, src, dst)

    def diff_analysis_graphs(self, before, after):
        """Before/after deltas for the improvement-loop stop conditions."""
        return _commands.diff(before, after)

    # --- Phase 7 reverse-engineering deliverables ---

    def generate_block_diagram(self, graph_source, direction: str | None = None) -> str:
        """Render the architecture block diagram (mermaid flowchart) from a graph.json."""
        direction = direction or self._config().deliverables.mermaid_direction
        return render_block_diagram(build_block_model(graph_source), direction)
