"""TDD tests for the SDK orchestration facade (8.016-8.027)."""

import inspect
from pathlib import Path

import pytest
from _orch_sdk import OrchSDK

from archlens.agents import (
    analyst_agent,
    bughunter_agent,
    graph_agent,
    metrics_agent,
    qa_agent,
    refactor_agent,
    repo_agent,
)
from archlens.sdk.dto_core import AnalysisReport
from archlens.sdk.dto_loop import LoopResult, TokenReport
from archlens.sdk.sdk import ArchLensSDK

FACTORIES = [
    repo_agent.make_repo_node, graph_agent.make_graph_node, analyst_agent.make_analyst_node,
    bughunter_agent.make_bughunter_node, refactor_agent.make_refactor_node,
    qa_agent.make_qa_node, metrics_agent.make_metrics_node,
]


@pytest.mark.parametrize("factory", FACTORIES)
def test_every_agent_factory_requires_injected_sdk(factory):
    params = list(inspect.signature(factory).parameters)
    assert params and params[0] == "sdk"


def test_no_module_level_subprocess_in_agents():
    agents_dir = Path(repo_agent.__file__).parent
    for py_file in agents_dir.glob("*.py"):
        text = py_file.read_text(encoding="utf-8")
        assert "import subprocess" not in text
        assert "subprocess." not in text


def test_sdk_builds_exactly_one_gatekeeper():
    sdk = ArchLensSDK()
    assert sdk._gk() is sdk._gk()


def test_sdk_loads_config_lazily():
    assert ArchLensSDK()._config().version == "1.00"


def test_analyze_returns_analysis_report(tmp_path):
    report = OrchSDK().analyze(db_path=str(tmp_path / "a.sqlite"), thread_id="a1")
    assert isinstance(report, AnalysisReport)
    assert report.node_count == 10
    assert "hub" in report.hubs
    assert "gate" in report.bottlenecks


def test_run_loop_returns_loop_result_within_cap(tmp_path):
    result = OrchSDK().run_loop(db_path=str(tmp_path / "l.sqlite"), thread_id="l1")
    assert isinstance(result, LoopResult)
    assert result.iterations <= 5
    assert result.stop_reason in ("hard_cap", "stop_conditions_met")


def test_measure_tokens_returns_token_report():
    report = OrchSDK().measure_tokens()
    assert isinstance(report, TokenReport)
    assert report.savings_pct == 70.0
    assert report.explanation_required is False


def test_measure_tokens_flags_explanation_below_seventy_percent():
    class _Low(OrchSDK):
        def token_usage(self):
            return {"baseline": 100, "assisted": 50}

    assert _Low().measure_tokens().explanation_required is True
