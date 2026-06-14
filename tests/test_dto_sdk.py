"""TDD tests for the Phase 8 SDK DTO dataclasses (tasks 8.009-8.011)."""

from dataclasses import FrozenInstanceError, is_dataclass

import pytest

from archlens.sdk.dto_core import AnalysisReport, GraphArtifacts, RepoSpec
from archlens.sdk.dto_loop import BugFinding, LoopResult, RefactorPlan, TokenReport

ALL_DTOS = [RepoSpec, GraphArtifacts, AnalysisReport, BugFinding, RefactorPlan, LoopResult, TokenReport]


@pytest.mark.parametrize("cls", ALL_DTOS)
def test_dto_is_a_frozen_dataclass(cls):
    assert is_dataclass(cls)
    assert cls.__dataclass_params__.frozen


def test_repo_spec_fields_and_immutability():
    spec = RepoSpec(url="u", branch="b", commit="c", workdir="w")
    assert (spec.url, spec.branch, spec.commit, spec.workdir) == ("u", "b", "c", "w")
    with pytest.raises(FrozenInstanceError):
        spec.url = "x"


def test_analysis_report_holds_tuples():
    report = AnalysisReport(node_count=5, edge_count=4, community_count=2,
                            hubs=("h",), bottlenecks=("b",), spofs=())
    assert report.hubs == ("h",)
    assert report.spofs == ()


def test_token_report_fields():
    report = TokenReport(baseline_tokens=100, assisted_tokens=30,
                         savings_pct=70.0, explanation_required=False)
    assert report.savings_pct == 70.0
    assert report.explanation_required is False
