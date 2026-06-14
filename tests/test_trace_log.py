"""TDD tests for the run-trace logger (tasks 10.041-10.043)."""

from archlens.agents.trace import TraceLogger, traced


def test_one_jsonl_record_per_transition(tmp_path):
    logger = TraceLogger(tmp_path / "t.jsonl")
    logger.record("RepoAgent", loop_iteration=1, duration_ms=5.0, tokens=100)
    records = logger.records()
    assert len(records) == 1
    assert set(records[0]) >= {"node", "loop_iteration", "duration_ms", "tokens"}
    assert records[0]["node"] == "RepoAgent"


def test_traced_wrapper_records_the_node(tmp_path):
    logger = TraceLogger(tmp_path / "t.jsonl")
    node = traced(lambda state: {"x": 1}, "GraphAgent", logger)
    assert node({"loop_iteration": 2}) == {"x": 1}
    record = logger.records()[0]
    assert record["node"] == "GraphAgent"
    assert record["loop_iteration"] == 2


def test_completeness_trace_lists_every_node_in_order(tmp_path):
    logger = TraceLogger(tmp_path / "t.jsonl")
    order = ["RepoAgent", "GraphAgent", "AnalystAgent", "BugHunterAgent"]
    for name in order:
        traced(lambda state: {}, name, logger)({})
    assert [r["node"] for r in logger.records()] == order
