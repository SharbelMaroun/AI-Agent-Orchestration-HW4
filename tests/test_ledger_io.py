"""TDD tests for TokenLedger JSONL persistence round-trip (task 12.006)."""

from pathlib import Path

import pytest

from archlens.metrics.ledger import TokenLedger
from archlens.metrics.ledger_io import (
    LedgerCorruptionError,
    ledger_path,
    load_ledger,
    save_ledger,
)
from archlens.metrics.ledger_model import TokenLedgerEntry
from archlens.shared.config import load_setup


def _ledger():
    return TokenLedger([
        TokenLedgerEntry(agent="RepoAgent", model="m1", protocol="baseline",
                         input_tokens=100, output_tokens=10, question_id="Q01"),
        TokenLedgerEntry(agent="GraphAgent", model="m2", protocol="assisted",
                         input_tokens=50, output_tokens=5, question_id="Q02"),
    ])


def test_save_then_load_round_trips(tmp_path):
    path = tmp_path / "out" / "ledger.jsonl"
    save_ledger(_ledger(), path)
    assert load_ledger(path).entries == _ledger().entries


def test_save_creates_parent_dirs(tmp_path):
    path = tmp_path / "deep" / "nested" / "ledger.jsonl"
    save_ledger(_ledger(), path)
    assert path.is_file()


def test_load_empty_ledger(tmp_path):
    path = tmp_path / "empty.jsonl"
    save_ledger(TokenLedger(), path)
    assert len(load_ledger(path)) == 0


def test_corrupt_line_raises(tmp_path):
    path = tmp_path / "bad.jsonl"
    path.write_text("{not valid json}\n", encoding="utf-8")
    with pytest.raises(LedgerCorruptionError):
        load_ledger(path)


def test_ledger_path_reads_from_config():
    expected = Path(load_setup().metrics.output_dir) / "baseline_ledger.jsonl"
    assert ledger_path("baseline_ledger.jsonl") == expected
