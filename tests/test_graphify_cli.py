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


def test_build_command_is_always_update():
    # Graphify has no `extract` command; `update` is the only structural build command.
    assert GraphifyCLI(_cfg("structural"), FakeGatekeeper()).command == "update"
    assert GraphifyCLI(_cfg("semantic"), FakeGatekeeper()).command == "update"


def test_run_delegates_to_gatekeeper():
    gk = FakeGatekeeper()
    out = GraphifyCLI(_cfg(), gk).run(Path("/repo"))
    assert out == "ok"
    argv, label, timeout = gk.calls[0]
    assert argv[:2] == ["graphify", "update"]
    assert label == "update"
    assert timeout == 600


def test_structural_runs_only_update_no_llm():
    gk = FakeGatekeeper()
    GraphifyCLI(_cfg("structural"), gk).run(Path("/repo"))
    assert [c[1] for c in gk.calls] == ["update"]  # no label / no LLM call


def test_semantic_also_labels_with_the_configured_gemini_model():
    gk = FakeGatekeeper()
    GraphifyCLI(_cfg("semantic"), gk).run(Path("/repo"))
    assert [c[1] for c in gk.calls] == ["update", "label"]
    label_argv = gk.calls[1][0]
    assert label_argv[:3] == ["graphify", "label", str(Path("/repo"))]
    assert "--backend" in label_argv and "gemini" in label_argv
    assert "gemini-3-flash-preview" in label_argv
