"""TDD tests for the agent handoff payload contracts (tasks 10.003-10.004)."""

import pytest
from pydantic import ValidationError

from archlens.agents.contracts import (
    FindingBatch,
    GraphSnapshotRef,
    MetricsDelta,
    PatchPlan,
    QAReport,
    RepoManifest,
)


def test_repo_manifest_parses():
    m = RepoManifest(local_path="/x", url="https://h/r", commit="abc", env_ready=True)
    assert m.commit == "abc"


def test_repo_manifest_rejects_unknown_key():
    with pytest.raises(ValidationError):
        RepoManifest(local_path="/x", url="u", commit="c", env_ready=True, bogus=1)


def test_graph_snapshot_ref_parses():
    s = GraphSnapshotRef(graph_json="g.json", node_count=5, edge_count=4,
                         report_md="R.md", snapshot_id=1)
    assert s.node_count == 5


def test_finding_batch_holds_findings():
    batch = FindingBatch(findings=[{"id": "f1"}])
    assert batch.findings[0]["id"] == "f1"


def test_patch_plan_requires_target_and_action():
    with pytest.raises(ValidationError):
        PatchPlan(action="split")


def test_qa_report_fields():
    qa = QAReport(tests_green=True, coverage_pct=97.0, ruff_violations=0)
    assert qa.tests_green is True


def test_metrics_delta_fields():
    delta = MetricsDelta(baseline_tokens=100, assisted_tokens=30, savings_pct=70.0)
    assert delta.savings_pct == 70.0


def test_qa_report_rejects_missing_field():
    with pytest.raises(ValidationError):
        QAReport(tests_green=True, coverage_pct=97.0)
