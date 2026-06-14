"""TDD tests for the gatekeeper concurrency limiter (task 9.020)."""

import threading
import time

from archlens.gatekeeper.concurrency import ConcurrencyLimiter
from archlens.gatekeeper.rate_config import load_rate_config, service_limits


def test_limiter_capacity_from_config():
    limits = service_limits(load_rate_config())
    assert ConcurrencyLimiter(limits.concurrent_max).capacity == 5


def test_max_in_flight_never_exceeds_capacity():
    limiter = ConcurrencyLimiter(5)
    state = {"in_flight": 0, "observed_max": 0}
    lock = threading.Lock()

    def work():
        with limiter:
            with lock:
                state["in_flight"] += 1
                state["observed_max"] = max(state["observed_max"], state["in_flight"])
            time.sleep(0.02)
            with lock:
                state["in_flight"] -= 1

    threads = [threading.Thread(target=work) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert state["observed_max"] == 5
