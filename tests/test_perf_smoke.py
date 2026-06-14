"""Performance smoke: the fully mocked end-to-end pipeline runs under a wall-clock budget (13.053).

Expected: the mocked supervisor pipeline completes well under 30 seconds.
"""

import time

from archlens.agents.runner import make_runner

BUDGET_SECONDS = 30.0


def test_mocked_pipeline_under_wall_clock_budget(tmp_path, mock_sdk, blocked_sockets):
    """Expected: make_runner + invoke complete within the 30-second budget on the mocked SDK."""
    graph = make_runner(mock_sdk, db_path=str(tmp_path / "perf.sqlite"))
    config = {"configurable": {"thread_id": "perf"}, "recursion_limit": 100}
    start = time.perf_counter()
    graph.invoke({}, config)
    elapsed = time.perf_counter() - start
    assert elapsed < BUDGET_SECONDS, f"pipeline took {elapsed:.1f}s (budget {BUDGET_SECONDS}s)"
