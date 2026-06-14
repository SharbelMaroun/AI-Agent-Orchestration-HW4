"""TDD tests for gatekeeper budget alerts (task 12.035)."""

from types import SimpleNamespace

from archlens.gatekeeper.gatekeeper import Gatekeeper
from archlens.shared.rate_limits import RateLimitsConfig


def _config(token_budget: int, alert_ratio: float = 0.8) -> RateLimitsConfig:
    return RateLimitsConfig.model_validate({
        "version": "1.00",
        "rate_limits": {"services": {"default": {
            "requests_per_minute": 30, "requests_per_hour": 500, "concurrent_max": 5,
            "retry_after_seconds": 30, "max_retries": 3}}},
        "queue": {"max_depth": 100, "backpressure_warn_ratio": 0.8},
        "budget": {"token_budget": token_budget, "alert_ratio": alert_ratio}})


class _Stub:
    def execute(self, model, messages, **kwargs):
        return SimpleNamespace(usage=SimpleNamespace(input_tokens=60, output_tokens=0))


def _call(gk):
    gk.execute("m", [{"role": "user", "content": "x"}], agent="A")


def test_alert_fires_when_crossing_threshold_but_call_completes():
    gk = Gatekeeper(config=_config(token_budget=100, alert_ratio=0.8), executor=_Stub())
    _call(gk)  # 60 tokens < 80 threshold -> no alert
    assert gk.budget_alerts == []
    _call(gk)  # 120 tokens >= 80 -> alert, call still completes
    assert len(gk.budget_alerts) == 1
    assert len(gk.usage_ledger.entries) == 2


def test_no_alert_below_threshold():
    gk = Gatekeeper(config=_config(token_budget=10_000), executor=_Stub())
    _call(gk)
    assert gk.budget_alerts == []


def test_budget_disabled_never_alerts_and_never_raises():
    gk = Gatekeeper(config=_config(token_budget=0), executor=_Stub())
    _call(gk)
    assert gk.budget_alerts == []
    assert len(gk.usage_ledger.entries) == 1
