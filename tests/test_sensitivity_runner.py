"""TDD tests for the OAT sensitivity runner (task 15.005)."""

import json

from archlens.metrics.sensitivity_runner import run_param_sweep


def test_run_param_sweep_writes_json_per_variant(tmp_path):
    variants = [{"top_k_pages": 1}, {"top_k_pages": 2}, {"top_k_pages": 3}]
    out = run_param_sweep("top_k_pages", variants,
                          lambda config: {"tokens": config["top_k_pages"] * 100}, tmp_path)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert out.name == "top_k_pages.json"
    assert data["param"] == "top_k_pages"
    assert len(data["records"]) == 3
    assert data["records"][0]["result"]["tokens"] == 100


def test_runner_invoked_once_per_variant(tmp_path):
    calls = []
    run_param_sweep("rate_limit_rpm", [{"rate_limit_rpm": 10}, {"rate_limit_rpm": 30}],
                    lambda config: calls.append(config) or {"ok": True}, tmp_path)
    assert len(calls) == 2
