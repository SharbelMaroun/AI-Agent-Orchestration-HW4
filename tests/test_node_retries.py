"""TDD tests for the per-node retry wrapper (tasks 10.039-10.040)."""

import pytest

from archlens.agents.retry import with_node_retry
from archlens.shared.exceptions import GatekeeperError

_NO_SLEEP = lambda _seconds: None  # noqa: E731


def test_transient_error_is_retried_then_succeeds():
    calls = {"n": 0}

    def node(state):
        calls["n"] += 1
        if calls["n"] < 3:
            raise GatekeeperError("rate limited", retryable=True)
        return {"ok": True}

    assert with_node_retry(node, max_retries=3, retry_after=0, sleep=_NO_SLEEP)({}) == {"ok": True}
    assert calls["n"] == 3


def test_permanent_error_surfaces_immediately():
    calls = {"n": 0}

    def node(state):
        calls["n"] += 1
        raise GatekeeperError("auth failed", retryable=False)

    with pytest.raises(GatekeeperError):
        with_node_retry(node, max_retries=3, retry_after=0, sleep=_NO_SLEEP)({})
    assert calls["n"] == 1


def test_transient_error_surfaces_after_max_retries():
    def node(state):
        raise GatekeeperError("always", retryable=True)

    with pytest.raises(GatekeeperError):
        with_node_retry(node, max_retries=2, retry_after=0, sleep=_NO_SLEEP)({})


def test_defaults_are_read_from_rate_limits_config():
    calls = {"n": 0}

    def node(state):
        calls["n"] += 1
        raise GatekeeperError("x", retryable=True)

    with pytest.raises(GatekeeperError):
        with_node_retry(node, retry_after=0, sleep=_NO_SLEEP)({})
    assert calls["n"] == 4  # 1 initial + max_retries(3) from config
