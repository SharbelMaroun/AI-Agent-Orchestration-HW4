"""TDD tests for the SDK Graphify facade methods (tasks 4.048-4.049)."""

from pathlib import Path

from archlens.graphops.diff import GraphDiff
from archlens.graphops.manifest import Manifest
from archlens.graphops.parser import Graph
from archlens.sdk.sdk import ArchLensSDK
from archlens.shared.config import load_setup

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "graphify"


class FakeGatekeeper:
    def __init__(self) -> None:
        self.commands: list[str] = []

    def run_graphify(self, argv, label, timeout_s):
        self.commands.append(label)
        return "ok"


def test_parse_graph_returns_graph_aggregate():
    sdk = ArchLensSDK(gatekeeper=FakeGatekeeper())
    graph = sdk.parse_graph(FIXTURES / "full.json")
    assert isinstance(graph, Graph)
    assert len(graph.nodes) == 6


def test_diff_graphs_returns_graphdiff():
    sdk = ArchLensSDK(gatekeeper=FakeGatekeeper())
    diff = sdk.diff_graphs(FIXTURES / "diff_before.json", FIXTURES / "diff_after.json")
    assert isinstance(diff, GraphDiff)
    assert diff.removed_edges == ["b->hub:calls"]


def test_run_pipeline_persists_manifest(setup_json, tmp_path: Path):
    cfg = load_setup(setup_json)
    cfg.graphify.output_root = str(tmp_path)
    sdk = ArchLensSDK(setup=cfg, gatekeeper=FakeGatekeeper())
    manifest = sdk.run_graphify_pipeline(Path("/repo"), run_id="run-test")
    assert isinstance(manifest, Manifest)
    assert manifest.stages[0].stage == "update"  # structural depth -> graphify update
    assert manifest.stages[0].status.value == "ok"
    assert (tmp_path / "run-test" / "manifest.json").is_file()
