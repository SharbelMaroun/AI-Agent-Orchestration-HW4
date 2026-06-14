"""Per-variant OAT sensitivity runner — one pipeline run per variant via an injected runner (15.006).

The runner callable is the SDK pipeline (or a stub in tests), so no external API call happens here
or outside the gatekeeper. Results are persisted to results/sensitivity/<param>.json.
"""

import json
from pathlib import Path


def run_param_sweep(param: str, variants: list[dict], runner, out_dir) -> Path:
    """Run ``runner(config)`` for each variant; write results/sensitivity/<param>.json; return path."""
    records = [{"config": config, "result": runner(config)} for config in variants]
    out = Path(out_dir) / f"{param}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"param": param, "records": records}, indent=2, sort_keys=True),
                   encoding="utf-8")
    return out
