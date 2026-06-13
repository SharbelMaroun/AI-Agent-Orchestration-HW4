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
