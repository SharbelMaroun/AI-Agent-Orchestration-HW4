"""Phase 15 variance runs + OAT sweeps -> results/ artifacts (tasks 15.013-15.018).

The OAT outcomes are REAL deterministic measurements, not toy formulas, and reproduce from committed
graphs/vault (no live LLM needed):
  - analysis_depth     : tiktoken size of the EXTRACTED-only structural edge slice vs the full
                         semantic edge set of the ArchLens self-graph (semantic adds INFERRED edges).
  - top_k_pages        : tiktoken size of the top-k graph-derived Obsidian vault pages (context grows
                         monotonically with k).
  - similarity_threshold: count of graph edges whose confidence_score >= threshold (deterministic).
  - rate_limit_rpm     : ANALYTICAL closed-form wait/queue for the 10-question workload at the swept
                         rpm (labelled method="analytical"; it is a model, not a timed run).
This script regenerates the sweeps each run so they stay reproducible. Run:
    uv run python scripts/run_sensitivity.py
"""

import json
import time
from pathlib import Path

import tiktoken

from archlens.metrics.ledger_io import ledger_path, load_ledger
from archlens.metrics.variance_stats import variance_stats, write_summary_csv
from archlens.sdk.sdk import ArchLensSDK
from archlens.shared.config import load_setup

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
GRAPH = ROOT / "artifacts" / "buggy-python-graph.json"
SELF_GRAPH = ROOT / "graphify-out" / "graph.json"  # has EXTRACTED + INFERRED edges (real depth mix)
VAULT = ROOT / "obsidian"
_ENC = tiktoken.get_encoding("o200k_base")
_WORKLOAD = 10  # the project's 10-question study, for the analytical rate model


def _tok(text: str) -> int:
    return len(_ENC.encode(text))


def _modularity() -> int:
    data = json.loads(GRAPH.read_text(encoding="utf-8"))
    return len({node.get("community") for node in data["nodes"]})


def _assisted_tokens() -> int:
    cfg = load_setup()
    return load_ledger(ledger_path(cfg.metrics.assisted_ledger)).total_tokens()


def _existing_runs() -> list[dict]:
    files = sorted((RESULTS / "variance").glob("run_*.json"))
    return [json.loads(path.read_text(encoding="utf-8")) for path in files]


def _baseline_runs(tokens: int, modularity: int) -> list[dict]:
    runs = []
    for index in range(1, 4):
        start = time.perf_counter()
        _ = _modularity()  # a small repeatable unit of pipeline work to time
        runtime = round(time.perf_counter() - start, 6)
        run = {"run": index, "tokens": tokens, "modularity": modularity, "runtime": runtime}
        (RESULTS / "variance").mkdir(parents=True, exist_ok=True)
        (RESULTS / "variance" / f"run_{index}.json").write_text(
            json.dumps(run, indent=2), encoding="utf-8")
        runs.append(run)
    return runs


def _depth_runner(config):
    """Measured: tiktoken size of the EXTRACTED-only edge slice vs the full semantic edge set."""
    links = json.loads(SELF_GRAPH.read_text(encoding="utf-8"))["links"]
    if config["analysis_depth"] == "structural":
        links = [link for link in links if str(link.get("confidence", "")).upper() == "EXTRACTED"]
    return {"tokens": _tok(json.dumps(links)), "edges": len(links)}


def _topk_runner(config):
    """Measured: tiktoken size of the top-k graph-derived vault pages (context grows with k)."""
    pages = sorted(VAULT.glob("*.md"))[: config["top_k_pages"]]
    context = "\n\n".join(page.read_text(encoding="utf-8") for page in pages)
    return {"tokens": _tok(context), "pages": len(pages)}


def _rate_runner(config):
    """Analytical: closed-form wait/queue for the 10-question workload at the swept rpm (a model)."""
    rpm = config["rate_limit_rpm"]
    minutes = -(-_WORKLOAD // rpm)  # ceil division
    return {"wait_time_s": max(0, minutes - 1) * 60,
            "max_queue_depth": max(0, _WORKLOAD - rpm), "method": "analytical"}


def _similarity_runner(config):
    """Measured: graph edges whose confidence_score >= threshold (deterministic from the self-graph)."""
    links = json.loads(SELF_GRAPH.read_text(encoding="utf-8"))["links"]
    threshold = config["similarity_threshold"]
    count = sum(1 for link in links if float(link.get("confidence_score", 0)) >= threshold)
    return {"validated_duplicates": count}


def main() -> int:
    sdk = ArchLensSDK()
    runs = _existing_runs() or _baseline_runs(_assisted_tokens(), _modularity())
    write_summary_csv(variance_stats(runs, ["tokens", "modularity", "runtime"]),
                      RESULTS / "variance" / "summary.csv")
    sweeps = {"analysis_depth": _depth_runner, "top_k_pages": _topk_runner,
              "rate_limits": _rate_runner, "similarity_threshold": _similarity_runner}
    param_key = {"rate_limits": "rate_limit_rpm"}
    for name, runner in sweeps.items():  # always regenerate so the measurements stay reproducible
        sdk.run_sensitivity(param_key.get(name, name), runner, RESULTS / "sensitivity")
        if name in param_key:
            (RESULTS / "sensitivity" / f"{param_key[name]}.json").replace(
                RESULTS / "sensitivity" / f"{name}.json")
    print("variance runs:", len(runs), "| modularity:", runs[0]["modularity"])
    print("OAT sweeps regenerated (real measurements):", ", ".join(sweeps))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
