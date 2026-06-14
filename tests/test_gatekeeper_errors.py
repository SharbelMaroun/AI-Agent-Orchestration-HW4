"""TDD tests for the gatekeeper error taxonomy (task 9.012)."""

from archlens.gatekeeper.errors import (
    ConfigVersionError,
    GatekeeperError,
    QueueSaturationSignal,
    RetryExhaustedSignal,
    UpstreamAPIError,
)


def test_gatekeeper_error_is_an_exception():
    assert issubclass(GatekeeperError, Exception)


def test_runtime_signals_subclass_the_base():
    assert issubclass(UpstreamAPIError, GatekeeperError)
    assert issubclass(RetryExhaustedSignal, GatekeeperError)
    assert issubclass(QueueSaturationSignal, GatekeeperError)


def test_config_version_error_is_a_value_error():
    assert issubclass(ConfigVersionError, ValueError)


def test_error_messages_are_preserved():
    assert "429" in str(UpstreamAPIError("429 rate limited"))


def test_signals_are_distinct_types():
    assert RetryExhaustedSignal is not QueueSaturationSignal
