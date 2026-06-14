"""TDD tests for the shared DTO JSON round-trip serializer (tasks 8.012-8.013)."""

import json

from archlens.sdk.dto_core import AnalysisReport, RepoSpec
from archlens.sdk.dto_loop import TokenReport
from archlens.shared.constants import DTO_SCHEMA_VERSION
from archlens.shared.serde import from_dict, to_dict


def test_to_dict_stamps_schema_version():
    assert to_dict(RepoSpec("u", "b", "c", "w"))["schema_version"] == DTO_SCHEMA_VERSION


def test_json_roundtrip_repo_spec():
    obj = RepoSpec("u", "b", "c", "w")
    assert from_dict(RepoSpec, json.loads(json.dumps(to_dict(obj)))) == obj


def test_json_roundtrip_analysis_report_restores_tuples():
    obj = AnalysisReport(5, 4, 2, ("h1", "h2"), ("b1",), ())
    assert from_dict(AnalysisReport, json.loads(json.dumps(to_dict(obj)))) == obj


def test_json_roundtrip_token_report():
    obj = TokenReport(100, 30, 70.0, False)
    assert from_dict(TokenReport, json.loads(json.dumps(to_dict(obj)))) == obj
