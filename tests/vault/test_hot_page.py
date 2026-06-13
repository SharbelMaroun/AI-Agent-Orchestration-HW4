"""TDD tests for the hot.md generator (tasks 5.014-5.020)."""

from pathlib import Path

from archlens.shared.constants import HOT_MAX_LINES
from archlens.vault.hot_page import render_hot

GOLDEN = Path(__file__).resolve().parent / "golden" / "hot.md"


def test_centrality_table(vault_graph, vault_cfg):
    hot = render_hot(vault_graph, vault_cfg)
    assert "## Top centrality nodes" in hot
    first_row = next(ln for ln in hot.splitlines() if ln.startswith("| checkout "))
    assert "[[payments]]" in first_row
    assert hot.index("| checkout ") < hot.index("| login ")  # descending by degree


def test_entry_points(vault_graph, vault_cfg):
    hot = render_hot(vault_graph, vault_cfg)
    section = hot.split("## Entry points")[1].split("##")[0]
    assert "cli_main" in section
    assert "[[payments]]" in section


def test_ambiguous_edges(vault_graph, vault_cfg):
    hot = render_hot(vault_graph, vault_cfg)
    section = hot.split("## Anomalies needing review")[1]
    assert "checkout -> login" in section
    assert "0.6" in section
    assert "src/payments/checkout.py" in section


def test_top_n_respected_and_within_line_budget(vault_graph, vault_cfg):
    hot = render_hot(vault_graph, vault_cfg)
    rows = [ln for ln in hot.splitlines() if ln.startswith("| ") and "[[" in ln]
    assert len(rows) <= vault_cfg.hot_top_n
    assert len(hot.splitlines()) <= HOT_MAX_LINES


def test_golden_file(vault_graph, vault_cfg):
    assert render_hot(vault_graph, vault_cfg) == GOLDEN.read_text(encoding="utf-8")
