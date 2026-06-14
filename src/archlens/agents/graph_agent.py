"""GraphAgent node — run the Graphify pipeline then build the Obsidian vault (task 5.044)."""

import logging

from archlens.shared.constants import LOGGER_NAME

logger = logging.getLogger(f"{LOGGER_NAME}.graph_agent")


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
        return {"graph_snapshot": {
            "graph_json": getattr(result, "graph_json", "graph.json"),
            "node_count": getattr(result, "node_count", 0),
            "edge_count": getattr(result, "edge_count", 0),
            "report_md": getattr(result, "report_md", "REPORT.md"),
            "snapshot_id": previous.get("snapshot_id", 0) + 1,
            "post_fix": bool(state.get("findings")),
            "diff": getattr(result, "diff", {}),
        }}

    return graph_node
