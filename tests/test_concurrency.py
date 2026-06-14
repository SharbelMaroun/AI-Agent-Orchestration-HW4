"""TDD tests for thread-safety of shared orchestration state (tasks 8.042-8.044)."""

import queue
from concurrent.futures import ThreadPoolExecutor

from archlens.metrics.counter import MetricsCounter
from archlens.sdk.plugins import PluginRegistry


def test_metrics_counter_is_thread_safe():
    counter = MetricsCounter()
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(lambda _: counter.add("calls"), range(1000)))
    assert counter.get("calls") == 1000


def test_plugin_registry_registration_is_thread_safe():
    registry = PluginRegistry()

    def register(index):
        registry.register_agent_plugin(f"p{index}", object())

    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(register, range(500)))
    assert len(registry.names()) == 500


def test_fifo_queue_is_thread_safe():
    fifo: queue.Queue = queue.Queue()
    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(fifo.put, range(1000)))
    assert fifo.qsize() == 1000


def test_thread_safety_soak_twenty_consecutive_runs():
    for _ in range(20):
        counter = MetricsCounter()
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(lambda _, c=counter: c.add("x"), range(200)))
        assert counter.get("x") == 200
