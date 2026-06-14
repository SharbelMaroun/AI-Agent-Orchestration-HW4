"""TDD tests for the gatekeeper RetryPolicy and retry-exhaustion handoff (tasks 9.022, 9.024)."""

import pytest

from archlens.gatekeeper.errors import RetryExhaustedSignal, UpstreamAPIError
from archlens.gatekeeper.rate_config import load_rate_config, service_limits
from archlens.gatekeeper.retry import RetryPolicy


def _policy(clock, max_retries=3, wait=30):
    return RetryPolicy(max_retries, wait, clock)


def test_success_needs_no_wait(fake_clock):
    assert _policy(fake_clock).run(lambda: "ok") == "ok"
    assert fake_clock.now() == 0.0


def test_waits_retry_after_between_attempts(fake_clock):
    attempts = []

    def op():
        attempts.append(1)
        if len(attempts) < 3:
            raise UpstreamAPIError("429")
        return "ok"

    assert _policy(fake_clock).run(op) == "ok"
    assert len(attempts) == 3
    assert fake_clock.now() == 60.0


def test_stops_after_max_retries(fake_clock):
    attempts = []

    def op():
        attempts.append(1)
        raise UpstreamAPIError("429")

    with pytest.raises(RetryExhaustedSignal):
        _policy(fake_clock).run(op)
    assert len(attempts) == 3


def test_exhaustion_requeues_without_propagating(fake_clock):
    requeued = []

    def op():
        raise UpstreamAPIError("429")

    result = _policy(fake_clock).run(op, on_exhausted=lambda err: requeued.append(err) or "queued")
    assert result == "queued"
    assert len(requeued) == 1


def test_from_config_uses_limit_values(fake_clock):
    policy = RetryPolicy.from_config(service_limits(load_rate_config()), fake_clock)
    with pytest.raises(RetryExhaustedSignal):
        policy.run(lambda: (_ for _ in ()).throw(UpstreamAPIError("429")))
    assert fake_clock.now() == 60.0
