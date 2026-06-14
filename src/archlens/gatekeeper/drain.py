"""Drain the overflow queue in FIFO order as window capacity frees (task 9.030).

Dispatches queued items head-first while the sliding window admits them; when the window is
saturated it waits out a full window via the Clock, then resumes — deterministic under FakeClock.
"""


def drain(queue, window, dispatch, clock) -> list:
    """Dispatch every queued item in FIFO order; return the dispatched items in order."""
    dispatched = []
    while queue.depth() > 0:
        if window.allow():
            item = queue.try_dequeue()
            dispatch(item)
            dispatched.append(item)
        else:
            clock.sleep(window.window_seconds)
    return dispatched
