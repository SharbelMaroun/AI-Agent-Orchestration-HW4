"""TDD test: GraphAgent builds the vault after the Graphify export (task 5.044)."""

from pathlib import Path

from archlens.agents.graph_agent import make_graph_agent
from archlens.sdk.sdk import ArchLensSDK
from archlens.shared.config import load_setup

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "vault" / "graph.json"


class FakeGatekeeper:
    def run_graphify_stage(self, argv, stage, timeout_s):
        return "ok"


def test_graph_agent_builds_vault(setup_json, tmp_path):
    cfg = load_setup(setup_json)
    cfg.vault.vault_root = str(tmp_path / "vault")
    cfg.graphify.output_root = str(tmp_path / "graphify")
    sdk = ArchLensSDK(setup=cfg, gatekeeper=FakeGatekeeper())
    state = {"target_repo": "/repo", "run_id": "r1", "graph_json": str(FIXTURE)}
    out = make_graph_agent(sdk)(state)
    assert (tmp_path / "vault" / "hot.md").is_file()
    assert (tmp_path / "vault" / "index.md").is_file()
    assert out["vault_root"].endswith("vault")
    assert out["graphify_run"] == "r1"
