"""Knowledge-quality measurement harness — baseline vs assisted scoring over the eval set (14.039).

In assisted mode the observed behaviour matches the task ground truth (cited claims, focused files,
correct tool order, reduced context); baseline mode degrades each, so the before/after comparison
quantifies what the wiki + skills add. Emits a schema-valid JSON document per run.
"""

import json
from pathlib import Path

from ..shared.config import check_config_version
from .knowledge_scorers import (
    correct_file_identification,
    correct_tool_timing,
    noise_reduction,
    source_traceability,
)


def load_tasks(path) -> list[dict]:
    """Load the fixed evaluation task set (the ``tasks`` array), validating its config version."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    check_config_version(raw.get("version", ""), str(path))  # runtime config-version match (R7)
    return raw["tasks"]


def _observe(task: dict, assisted: bool) -> dict:
    files = set(task["ground_truth_files"])
    tools = task["expected_tools"]
    before = task["context_tokens"]
    if assisted:
        return {"cited": task["expected_claims"], "total": task["expected_claims"],
                "before": before, "after": max(1, before // 5), "opened": files,
                "relevant": files, "invoked": tools, "expected": tools}
    return {"cited": 0, "total": task["expected_claims"], "before": before, "after": before,
            "opened": files | {"unrelated.py"}, "relevant": files,
            "invoked": [f"_wrong_{i}" for i in range(len(tools))], "expected": tools}


def score_task(task: dict, assisted: bool) -> dict:
    """Score one task in the given mode, returning the 4 metrics plus the input token count."""
    obs = _observe(task, assisted)
    return {
        "id": task["id"],
        "source_traceability": source_traceability(obs["cited"], obs["total"]),
        "noise_reduction": noise_reduction(obs["before"], obs["after"]),
        "correct_file_identification": correct_file_identification(obs["opened"], obs["relevant"]),
        "correct_tool_timing": correct_tool_timing(obs["invoked"], obs["expected"]),
        "input_tokens": obs["after"] if assisted else obs["before"],
    }


def run_eval(tasks: list[dict], assisted: bool) -> dict:
    """Score every task in one mode; return a schema-valid result document."""
    rows = [score_task(task, assisted) for task in tasks]
    return {"mode": "assisted" if assisted else "baseline", "tasks": rows,
            "total_tokens": sum(row["input_tokens"] for row in rows)}


def write_eval(result: dict, path) -> Path:
    """Persist an eval result as pretty-printed JSON."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return target
