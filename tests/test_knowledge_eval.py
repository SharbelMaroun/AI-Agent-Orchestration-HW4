"""TDD tests for the knowledge measurement harness (task 14.038)."""

from archlens.metrics.knowledge_eval import load_tasks, run_eval, score_task, write_eval
from archlens.shared.constants import RUBRIC_METRICS

TASKS = "config/eval_tasks.json"


def test_load_tasks_has_ten():
    assert len(load_tasks(TASKS)) == 10


def test_run_eval_records_four_scores_and_tokens_per_task():
    result = run_eval(load_tasks(TASKS), assisted=True)
    assert result["mode"] == "assisted"
    assert len(result["tasks"]) == 10
    for row in result["tasks"]:
        for metric in RUBRIC_METRICS:
            assert 0 <= row[metric] <= 10
        assert row["input_tokens"] > 0


def test_assisted_beats_baseline_and_uses_fewer_tokens():
    tasks = load_tasks(TASKS)
    base, asst = run_eval(tasks, assisted=False), run_eval(tasks, assisted=True)
    base_total = sum(row[m] for row in base["tasks"] for m in RUBRIC_METRICS)
    asst_total = sum(row[m] for row in asst["tasks"] for m in RUBRIC_METRICS)
    assert asst_total > base_total
    assert asst["total_tokens"] < base["total_tokens"]


def test_score_task_and_write_round_trip(tmp_path):
    task = load_tasks(TASKS)[0]
    row = score_task(task, assisted=True)
    assert row["id"] == "E01"
    out = write_eval({"mode": "assisted", "tasks": [row], "total_tokens": 1},
                     tmp_path / "k.json")
    assert out.is_file()
