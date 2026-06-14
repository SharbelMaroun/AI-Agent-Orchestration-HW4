"""Chart factory — bar/line/scatter/heatmap/box/waterfall PNG renderers, Agg backend (task 15.010)."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402  (backend must be set before pyplot import)


def _save(path) -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(target)
    plt.close()
    return target


def bar_chart(labels, values, path, title="", ylabel="") -> Path:
    """A simple vertical bar chart."""
    plt.figure(figsize=(8, 5))
    plt.bar([str(label) for label in labels], values)
    plt.title(title)
    plt.ylabel(ylabel)
    return _save(path)


def line_chart(xs, ys, path, title="", ylabel="") -> Path:
    """A line plot with markers."""
    plt.figure(figsize=(8, 5))
    plt.plot(xs, ys, marker="o")
    plt.title(title)
    plt.ylabel(ylabel)
    return _save(path)


def scatter_chart(xs, ys, path, title="", annotate_x=None) -> Path:
    """A scatter plot, optionally annotating a vertical line at annotate_x."""
    plt.figure(figsize=(8, 5))
    plt.scatter(xs, ys)
    if annotate_x is not None:
        plt.axvline(annotate_x, color="red", linestyle="--")
    plt.title(title)
    return _save(path)


def heatmap_chart(matrix, row_labels, col_labels, path, title="") -> Path:
    """A heatmap with a colorbar legend over a 2D matrix."""
    plt.figure(figsize=(8, 5))
    plt.imshow(matrix, aspect="auto", cmap="viridis")
    plt.yticks(range(len(row_labels)), row_labels)
    plt.xticks(range(len(col_labels)), col_labels)
    plt.colorbar()
    plt.title(title)
    return _save(path)


def box_chart(series: dict, path, title="") -> Path:
    """A box plot, one box per named series."""
    plt.figure(figsize=(8, 5))
    plt.boxplot(list(series.values()), tick_labels=list(series.keys()))
    plt.title(title)
    return _save(path)


def waterfall_chart(stages, deltas, path, title="") -> Path:
    """A cumulative waterfall: each stage's contribution stacked onto the running total."""
    plt.figure(figsize=(9, 5))
    running = 0
    for stage, delta in zip(stages, deltas, strict=True):
        plt.bar(str(stage), delta, bottom=running)
        running += delta
    plt.title(title)
    return _save(path)
