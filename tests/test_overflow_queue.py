"""TDD tests for the FIFO overflow queue and blocking backpressure (tasks 9.025, 9.027)."""

import threading
import time

from archlens.gatekeeper.overflow_queue import OverflowQueue
from archlens.gatekeeper.rate_config import load_rate_config


def test_strict_fifo_order():
    queue = OverflowQueue(10)
    for i in range(5):
        queue.enqueue(i)
    assert [queue.try_dequeue() for _ in range(5)] == [0, 1, 2, 3, 4]


def test_depth_gauge_tracks_size():
    queue = OverflowQueue(10)
    queue.enqueue("x")
    queue.enqueue("y")
    assert queue.depth() == 2
    queue.try_dequeue()
    assert queue.depth() == 1


def test_max_depth_from_config():
    queue = OverflowQueue(load_rate_config().queue.max_depth)
    assert queue.capacity == 100


def test_backpressure_blocks_until_space_frees_no_drops():
    queue = OverflowQueue(2)
    queue.enqueue("a")
    queue.enqueue("b")
    done = threading.Event()

    def producer():
        queue.enqueue("c")
        done.set()

    thread = threading.Thread(target=producer)
    thread.start()
    time.sleep(0.05)
    assert not done.is_set()
    assert queue.dequeue() == "a"
    thread.join(timeout=1)
    assert done.is_set()
    assert queue.dropped_count == 0
    assert [queue.try_dequeue(), queue.try_dequeue()] == ["b", "c"]
