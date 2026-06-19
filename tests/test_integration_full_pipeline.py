"""Integration: full pipeline terminates; sample_repo seeds god + duplicate (10.051-10.052)."""

from pathlib import Path

from archlens.agents.runner import make_runner

SAMPLE = Path(__file__).resolve().parent / "fixtures" / "sample_repo"


def test_sample_repo_seeds_god_module_and_duplicate_pair():
    importers = [p for p in SAMPLE.glob("*.py") if "import core" in p.read_text(encoding="utf-8")]
    assert len(importers) >= 3
    body1 = (SAMPLE / "dup1.py").read_text(encoding="utf-8")
    body2 = (SAMPLE / "dup2.py").read_text(encoding="utf-8")
    assert body1 == body2


def test_full_pipeline_terminates_within_five_iterations(tmp_path, mock_sdk, blocked_sockets):
    # Autonomous loop: the irreversible-fix approval gate runs under the auto-grant policy so the
    # loop progresses without a human (the interactive gate would correctly pause for input instead).
    graph = make_runner(mock_sdk, db_path=str(tmp_path / "f.sqlite"), auto_approve=True)
    config = {"configurable": {"thread_id": "f1"}, "recursion_limit": 150}
    graph.invoke({}, config)
    state = graph.get_state({"configurable": {"thread_id": "f1"}}).values
    assert state.get("loop_iteration", 0) <= 5
    assert state.get("stop_eval", {}).get("met") or state.get("loop_iteration") == 5
