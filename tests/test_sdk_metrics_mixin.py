"""Tests for the SDK MetricsMixin entry points (tasks 13.022/13.023 — lift sdk coverage >= 95%).

Expected: load_questions, run_baseline, run_assisted, and export_token_metrics work via the SDK.
"""

from pathlib import Path

from archlens.sdk.sdk import ArchLensSDK

FIXTURES = Path(__file__).resolve().parent / "fixtures"
MINI = FIXTURES / "mini_repo"


def test_load_questions_returns_ten():
    """Expected: the SDK exposes the 10 standard questions."""
    assert len(ArchLensSDK().load_questions()) == 10


def test_run_baseline_offline_estimating_gatekeeper():
    """Expected: run_baseline builds the estimating gatekeeper and tags entries baseline."""
    ledger = ArchLensSDK().run_baseline(MINI)
    assert len(ledger.entries) == 10
    assert {entry.protocol for entry in ledger.entries} == {"baseline"}


def test_run_assisted_over_fake_vault(fake_vault_fs):
    """Expected: run_assisted answers all questions from the vault, tagged assisted."""
    ledger = ArchLensSDK().run_assisted(vault_root=fake_vault_fs)
    assert len(ledger.entries) == 10
    assert {entry.protocol for entry in ledger.entries} == {"assisted"}


def test_metrics_gatekeeper_is_constructed():
    """Expected: the SDK can build a dedicated estimating metrics gatekeeper."""
    from archlens.gatekeeper.gatekeeper import Gatekeeper
    assert isinstance(ArchLensSDK()._metrics_gatekeeper(), Gatekeeper)


def test_metrics_gatekeeper_live_builds_real_mode_gatekeeper():
    """Expected: live=True yields a real-API-mode gatekeeper (no network until a call is made)."""
    from archlens.gatekeeper.gatekeeper import Gatekeeper
    gk = ArchLensSDK()._metrics_gatekeeper(live=True)
    assert isinstance(gk, Gatekeeper)


def test_export_token_metrics_writes_and_returns(tmp_path, fake_vault_fs):
    """Expected: export_token_metrics writes the json file and returns the full schema dict."""
    sdk = ArchLensSDK()
    baseline = sdk.run_baseline(MINI)
    assisted = sdk.run_assisted(vault_root=fake_vault_fs)
    out = tmp_path / "token_metrics.json"
    metrics = sdk.export_token_metrics(baseline, assisted, graph_build_tokens=1000, path=out)
    assert out.is_file()
    assert "per_model" in metrics
    assert "savings" in metrics
