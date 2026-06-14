"""TDD tests for the drain loop and FIFO requeue ordering (tasks 9.029, 9.031)."""

from archlens.gatekeeper.drain import drain
from archlens.gatekeeper.overflow_queue import OverflowQueue
from archlens.gatekeeper.rate_config import load_rate_config, service_limits
from archlens.gatekeeper.windows import minute_window


def _limits():
    return service_limits(load_rate_config())


def test_drain_dispatches_in_fifo_order(fake_clock):
    queue = OverflowQueue(50)
    for i in range(5):
        queue.enqueue(i)
    dispatched = []
    drain(queue, minute_window(_limits(), fake_clock), dispatched.append, fake_clock)
    assert dispatched == [0, 1, 2, 3, 4]
    assert queue.depth() == 0


def test_drain_waits_for_window_then_dispatches_all(fake_clock):
    queue = OverflowQueue(200)
    for i in range(35):
        queue.enqueue(i)
    dispatched = []
    drain(queue, minute_window(_limits(), fake_clock), dispatched.append, fake_clock)
    assert dispatched == list(range(35))
    assert fake_clock.now() >= 60


def test_requeue_order_enters_at_tail(fake_clock):
    queue = OverflowQueue(10)
    for item in (1, 2, 3):
        queue.enqueue(item)
    queue.enqueue(99)  # a requeued request re-enters at the tail
    dispatched = []
    drain(queue, minute_window(_limits(), fake_clock), dispatched.append, fake_clock)
    assert dispatched == [1, 2, 3, 99]
