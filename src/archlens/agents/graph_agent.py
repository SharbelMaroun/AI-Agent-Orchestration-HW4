"""GraphAgent node — run the Graphify pipeline then build the Obsidian vault (task 5.044)."""

import json
import logging
from pathlib import Path

from ..shared.constants import (
    GRAPH_JSON,
    GRAPHIFY_OUT_DIR,
    GRAPHIFY_REPORT_MD,
    LOGGER_NAME,
)

logger = logging.getLogger(f"{LOGGER_NAME}.graph_agent")


def _out_dir(repo: str) -> Path:
    """Graphify writes graph.json/graph.html/GRAPH_REPORT.md to ``<repo>/graphify-out/``."""
    return Path(repo) / GRAPHIFY_OUT_DIR


def _counts(result, graph_json: str) -> tuple[int, int]:
    """Node/edge counts: prefer explicit result attrs, else read the produced graph.json."""
    nodes, edges = getattr(result, "node_count", None), getattr(result, "edge_count", None)
    if nodes is not None and edges is not None:
        return nodes, edges
    try:
        data = json.loads(Path(graph_json).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return nodes or 0, edges or 0
    return len(data.get("nodes", [])), len(data.get("links", data.get("edges", [])))


def make_graph_agent(sdk):
    """Factory: bind the SDK and return the node callable (state in -> state delta out)."""

    def graph_agent(state: dict) -> dict:
        manifest = sdk.run_graphify_pipeline(state["target_repo"], run_id=state.get("run_id"))
        graph_json = state.get("graph_json")
        layout = sdk.build_vault(graph_json) if graph_json else None
        logger.info("graph agent finished run %s; vault=%s", manifest.run_id, bool(layout))
        return {
            "graphify_run": manifest.run_id,
            "vault_root": str(layout.root) if layout else None,
        }

    return graph_agent


def make_graph_node(sdk):
    """Orchestration node: run Graphify via the SDK and store a graph_snapshot (10.016)."""

    def graph_node(state: dict) -> dict:
        repo = state["target_repo"]["local_path"]
        result = sdk.run_graphify_pipeline(repo)
        previous = state.get("graph_snapshot") or {}
        graph_json = getattr(result, "graph_json", None) or str(_out_dir(repo) / GRAPH_JSON)
        nodes, edges = _counts(result, graph_json)
        return {"graph_snapshot": {
            "graph_json": graph_json,
            "node_count": nodes,
            "edge_count": edges,
            "report_md": getattr(result, "report_md", None) or str(
                _out_dir(repo) / GRAPHIFY_REPORT_MD),
            "snapshot_id": previous.get("snapshot_id", 0) + 1,
            "post_fix": bool(state.get("findings")),
            "diff": getattr(result, "diff", {}),
        }}

    return graph_node
