"""QAAgent node — run tests/coverage/ruff via the SDK and write stop_eval inputs (10.024)."""


def make_qa_node(sdk):
    """Factory: bind the SDK and return the QA node writing QA results into stop_eval."""

    def qa_node(state: dict) -> dict:
        report = sdk.run_quality_gates(state.get("target_repo", {}).get("local_path"))
        stop_eval = dict(state.get("stop_eval") or {})
        stop_eval["tests_green"] = bool(report.tests_green)
        stop_eval["coverage_pct"] = report.coverage_pct
        stop_eval["ruff_zero"] = report.ruff_violations == 0
        return {"stop_eval": stop_eval}

    return qa_node
