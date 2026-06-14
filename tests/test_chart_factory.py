"""TDD tests for the chart factory PNG renderers (task 15.009)."""

import pytest

from archlens.metrics.chart_factory import (
    bar_chart,
    box_chart,
    heatmap_chart,
    line_chart,
    scatter_chart,
    waterfall_chart,
)

CASES = [
    ("bar", lambda p: bar_chart(["a", "b"], [1, 2], p)),
    ("line", lambda p: line_chart([1, 2, 3], [1, 4, 9], p)),
    ("scatter", lambda p: scatter_chart([1, 2, 3], [3, 2, 1], p, annotate_x=0.91)),
    ("heatmap", lambda p: heatmap_chart([[1, 2], [3, 4]], ["r1", "r2"], ["c1", "c2"], p)),
    ("box", lambda p: box_chart({"x": [1, 2, 3], "y": [2, 3, 4]}, p)),
    ("waterfall", lambda p: waterfall_chart(["s1", "s2"], [5, 3], p)),
]


@pytest.mark.parametrize("name, call", CASES)
def test_chart_writes_non_empty_png(tmp_path, name, call):
    out = call(tmp_path / f"{name}.png")
    assert out.is_file()
    assert out.stat().st_size > 0
