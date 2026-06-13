"""TDD tests for GraphifyCLI real-command construction + gatekeeper delegation (4.011-4.013)."""

from pathlib import Path

from archlens.graphops.cli_wrapper import GraphifyCLI, build_argv
from archlens.graphops.config import GraphifyConfig


def _cfg(depth: str = "structural") -> GraphifyConfig:
    return GraphifyConfig.model_validate(
        {
            "binary": "graphify",
            "stages": ["detect", "extract", "build", "cluster", "export"],
            "output_root": "runs/graphify",
            "timeout_s": 600,
            "analysis_depth": depth,
            "token_budget": 100000,
        }
    )


class FakeGatekeeper:
    def __init__(self) -> None:
        self.calls: list[tuple] = []

    def run_graphify(self, argv, label, timeout_s):
        self.calls.append((argv, label, timeout_s))
        return "ok"


def test_build_argv_uses_real_graphify_command():
    assert build_argv(_cfg(), "update", Path("/repo")) == ["graphify", "update", str(Path("/repo"))]


def test_structural_uses_update_and_semantic_uses_extract():
    assert GraphifyCLI(_cfg("structural"), FakeGatekeeper()).command == "update"
    assert GraphifyCLI(_cfg("semantic"), FakeGatekeeper()).command == "extract"


def test_run_delegates_to_gatekeeper():
    gk = FakeGatekeeper()
    out = GraphifyCLI(_cfg(), gk).run(Path("/repo"))
    assert out == "ok"
    argv, label, timeout = gk.calls[0]
    assert argv[:2] == ["graphify", "update"]
    assert label == "update"
    assert timeout == 600
