"""Tests for the EX04 graph-guided debug-demo report."""

from archlens.sdk.sdk import ArchLensSDK


def test_debug_demo_outputs_assignment_evidence():
    report = ArchLensSDK().debug_demo()
    assert "lambda_array" in report
    assert "snippets/__init__.py" in report
    assert "BugLocalizer" in report
    assert "deliverables/buggy-python-fix.patch" in report
    assert "deliverables/BUG_REPORT.md" in report
    assert "obsidian/localization.md" in report
    assert "metrics/out/debug_token_study.json" in report


def test_submission_demo_outputs_full_grader_path():
    report = ArchLensSDK().submission_demo()
    assert "RepoAgent -> GraphAgent" in report
    assert "BugLocalizer/BugHunterAgent" in report
    assert "deliverables/buggy-python-fix.patch" in report
    assert "uv run pytest --cov=archlens --cov-branch" in report
