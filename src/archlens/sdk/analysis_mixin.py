"""Phase 6 graph-analysis facade methods, mixed into ArchLensSDK (keeps sdk.py within 150 lines).

The mixin delegates to graphops modules so external callers never import graphops directly.
"""

from ..graphops import commands as _commands
from ..graphops.bridges import bridge_report
from ..graphops.centrality import degree_centrality
from ..graphops.classify import classify
from ..graphops.communities import community_folder_mismatches, detect_communities
from ..graphops.duplicates import route_duplicates_to_review
from ..graphops.graph_metrics import modularity
from ..graphops.loader import load_graph
from ..graphops.spof import critical_paths, spof_detect
from ..graphops.triage import triage_edges
from ..graphops.views import macro_view, meso_view, micro_view


class GraphAnalysisMixin:
    """Single-entry SDK methods for the Phase 6 graph-analysis engine."""

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

    def localize_bug(self, graph_source, failing_symbol: str):
        """Graph-first localization of an import failure to its suspect node + root cause (EX04 §5.3)."""
        from ..agents.bug_localizer import localize_import_failure
        return localize_import_failure(graph_source, failing_symbol)

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
