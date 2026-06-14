"""Green baseline suite for the loop_target convergence fixture (task 11.048)."""

from core import serve
from feature_a import run as run_a
from feature_b import run as run_b


def test_core_serves():
    assert serve(1)["ok"] is True


def test_features_agree():
    assert run_a([1, 2, 3]) == run_b([1, 2, 3])


def test_compute_total_doubles_and_sums():
    assert run_a([2, 3])["payload"] == 10
