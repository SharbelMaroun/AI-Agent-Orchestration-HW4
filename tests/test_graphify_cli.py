"""TDD tests for GraphifyCLI argv construction and gatekeeper delegation (tasks 4.011-4.013)."""

from pathlib import Path

from archlens.graphops.cli_wrapper import GraphifyCLI, build_argv
from archlens.graphops.config import GraphifyConfig

CFG = GraphifyConfig.model_validate(
    {
        "binary": "graphify",
        "stages": ["detect", "extract", "build", "cluster", "export"],
        "output_root": "runs/graphify",
        "timeout_s": 600,
        "analysis_depth": "structural",
        "token_budget": 100000,
    }
)


class FakeGatekeeper:
    def __init__(self) -> None:
        self.calls: list[tuple] = []

    def run_graphify_stage(self, argv, stage, timeout_s):
        self.calls.append((argv, stage, timeout_s))
        return "ok"


def test_build_argv_is_exact():
    argv = build_argv(CFG, "extract", Path("/tmp/repo"))
    assert argv == [
        "uv",
        "run",
        "graphify",
        "--stage",
        "extract",
        "--repo",
        str(Path("/tmp/repo")),
        "--depth",
        "structural",
    ]


def test_cli_delegates_each_stage_to_gatekeeper():
    gk = FakeGatekeeper()
    out = GraphifyCLI(CFG, gk).run_stage("build", Path("/tmp/repo"))
    assert out == "ok"
    assert gk.calls[0][1] == "build"
    assert gk.calls[0][2] == 600
