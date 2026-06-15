"""The SDK single-entry QA gate delegates to the dependency-free module gate."""

from archlens.agents.contracts import QAReport
from archlens.sdk.sdk import ArchLensSDK


def test_sdk_run_quality_gates_parses_a_clean_tree(tmp_path):
    (tmp_path / "m.py").write_text("value = 1\n", encoding="utf-8")
    report = ArchLensSDK().run_quality_gates(str(tmp_path))
    assert isinstance(report, QAReport)
    assert report.tests_green is True
    assert report.ruff_violations == 0
