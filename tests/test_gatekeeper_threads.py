"""TDD thread-safety test for the gatekeeper under contention (task 9.046)."""

import threading

from archlens.gatekeeper.clock import FakeClock
from archlens.gatekeeper.executor import RateLimitedExecutor
from archlens.gatekeeper.mock_client import MockAnthropicClient
from archlens.gatekeeper.rate_config import load_rate_config


def test_50_threads_20_calls_record_1000_consistent_entries(rate_config_factory):
    config = load_rate_config(
        rate_config_factory(requests_per_minute=100000, requests_per_hour=1000000))
    executor = RateLimitedExecutor(MockAnthropicClient(), FakeClock(), config)

    def worker():
        for _ in range(20):
            executor.execute("m", [])

    threads = [threading.Thread(target=worker) for _ in range(50)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(executor.ledger.entries) == 1000
    assert executor.dispatched == 1000
    assert executor.window_counts == (1000, 1000)
