"""TDD tests for the AgentState schema and its reducers (tasks 10.001-10.002)."""

import typing

import pytest

from archlens.agents.state import AgentState, append_records

KEYS = [
    "target_repo", "graph_snapshot", "findings", "loop_iteration",
    "stop_eval", "token_ledger", "approvals",
]


@pytest.mark.parametrize("key", KEYS)
def test_state_exposes_typed_key(key):
    assert key in AgentState.__annotations__


def test_append_reducer_accumulates_and_handles_none():
    assert append_records(["a"], ["b"]) == ["a", "b"]
    assert append_records(None, ["b"]) == ["b"]
    assert append_records(["a"], None) == ["a"]


def test_findings_and_approvals_use_the_append_reducer():
    hints = typing.get_type_hints(AgentState, include_extras=True)
    for key in ("findings", "approvals"):
        assert typing.get_args(hints[key])[1] is append_records


def test_token_ledger_is_last_write_wins():
    hints = typing.get_type_hints(AgentState, include_extras=True)
    assert hints["token_ledger"] is dict
