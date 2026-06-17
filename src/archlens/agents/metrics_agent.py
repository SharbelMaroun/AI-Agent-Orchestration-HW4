"""MetricsAgent node — append token/cost rows to state.token_ledger via the SDK (10.026)."""


def make_metrics_node(sdk):
    """Factory: bind the SDK and return the metrics node computing token deltas and cost rows."""

    def metrics_node(state: dict) -> dict:
        usage = sdk.token_usage()
        baseline = usage.get("baseline", 0)
        assisted = usage.get("assisted", 0)
        ledger = dict(state.get("token_ledger") or {})
        ledger["baseline_tokens"] = baseline
        ledger["assisted_tokens"] = assisted
        ledger["savings_pct"] = round(100.0 * (1 - assisted / baseline), 1) if baseline else 0.0
        ledger["total_tokens"] = usage.get("total", assisted)  # real tokens the run consumed
        ledger["input_tokens"] = usage.get("input", 0)
        ledger["output_tokens"] = usage.get("output", 0)
        ledger["rows"] = usage.get("rows", [])
        return {"token_ledger": ledger}

    return metrics_node
