"""Reference tests for public helpers exercised only transitively elsewhere (supports task 13.025).

These functions are reached through higher-level entry points in other suites; this module references
each one directly so the public-API meta-test sees explicit test coverage of every public callable.

Expected: every listed public helper imports and is callable.
"""

from archlens.agents.refactor_rewire import extract_def, make_seam, rewrite_import
from archlens.gatekeeper.git_ops import run_local_git
from archlens.gatekeeper.graphify_ops import run_command
from archlens.gatekeeper.proc import run_capture
from archlens.graphops.rerun import iteration_output_dir
from archlens.graphops.thresholds import thresholds
from archlens.metrics.charts import baseline_vs_assisted_bar, savings_waterfall
from archlens.metrics.graph_diff import isolated_nodes
from archlens.shared.config import check_config_version
from archlens.shared.validators import bounded_confidence
from archlens.vault.community_pages import render_community
from archlens.vault.graphview import (
    anomalies,
    community_of,
    connector_labels,
    degree_scores,
    ranked_nodes,
)


def test_public_helpers_are_callable():
    """Expected: each transitively-tested public helper is importable and callable."""
    helpers = [extract_def, make_seam, rewrite_import, run_local_git, run_command, run_capture,
               isolated_nodes, iteration_output_dir, thresholds, baseline_vs_assisted_bar,
               savings_waterfall, check_config_version, bounded_confidence, render_community,
               anomalies, community_of, connector_labels, degree_scores, ranked_nodes]
    assert all(callable(helper) for helper in helpers)
