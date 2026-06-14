"""TDD tests for the Gatekeeper.execute() facade and never-reject invariants (9.042, 9.044, 9.045)."""

from archlens.gatekeeper.clock import FakeClock
from archlens.gatekeeper.executor import RateLimitedExecutor
from archlens.gatekeeper.gatekeeper import Gatekeeper
from archlens.gatekeeper.mock_client import MockAnthropicClient
from archlens.gatekeeper.rate_config import load_rate_config

_MSG = [{"role": "user", "content": "hi"}]


def _executor(clock=None, config=None):
    return RateLimitedExecutor(MockAnthropicClient(), clock or FakeClock(), config or load_rate_config())


def test_immediate_capacity_returns_response():
    executor = _executor()
    response = executor.execute("claude-opus-4-8", _MSG)
    assert response.status == 200
    assert executor.dispatched == 1


def test_saturation_30_dispatch_10_queue_0_reject():
    executor = _executor()
    admitted = [executor.submit("m", []) for _ in range(40)]
    assert sum(admitted) == 30
    assert executor.dispatched == 30
    assert executor.queue_depth == 10
    assert executor.dropped == 0


def test_never_reject_600_requests_all_complete():
    executor = _executor()
    responses = [executor.execute("m", []) for _ in range(600)]
    assert all(response is not None for response in responses)
    assert executor.dispatched == 600
    assert executor.queue_depth == 0
    assert executor.dropped == 0


def test_gatekeeper_execute_immediate_path():
    gatekeeper = Gatekeeper(executor=_executor())
    assert gatekeeper.execute("claude-opus-4-8", _MSG).status == 200


def test_gatekeeper_execute_saturated_path_queues_then_completes():
    executor = _executor()
    for _ in range(30):
        executor.submit("m", [])
    response = Gatekeeper(executor=executor).execute("m", _MSG)
    assert response.status == 200
    assert executor.queue_depth == 0


def test_default_gatekeeper_execute_runs_in_mock_mode():
    assert Gatekeeper().execute("claude-opus-4-8", _MSG).status == 200
