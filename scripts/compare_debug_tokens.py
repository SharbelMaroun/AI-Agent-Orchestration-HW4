"""Token study for the EX04 debugging task: naive raw-file reading vs graph-guided context (§5.5).

Both modes answer the SAME question — "which file must be fixed FIRST to resolve the import failure?"
— over the andela/buggy-python clone, and we report all four axes the spec lists:
  - tokens consumed (gatekeeper ledger), - files / text units read,
  - iterations / investigation cycles, - quality (did it reach the correct root cause: the hub).
NAIVE is the spec's unfocused baseline (dump the whole repo); its cycle count is how many files a
LINEAR one-at-a-time scan must reveal before the hub is named. GRAPH-GUIDED reads the two graph-derived
vault pages once. Writes metrics/out/debug_token_study.json. Needs a live key in .env.

    uv run python scripts/compare_debug_tokens.py
"""

import json
from pathlib import Path

from archlens.sdk.sdk import ArchLensSDK

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT / "runs" / "buggy-python"
OUT = ROOT / "metrics" / "out" / "debug_token_study.json"
NAIVE_ORDER = ["main.py", "snippets/__init__.py", "snippets/loop.py", "snippets/io.py", "snippets/foobar.py"]
ASK = "Which single file must be fixed FIRST to resolve the import failure? Answer just the path, or UNKNOWN."


def _ask(sdk, prompt: str, agent: str) -> str:
    return sdk.ask_llm(prompt, agent=agent, max_tokens=60)


def _correct(answer: str) -> bool:
    """The correct first fix is the re-export hub snippets/__init__.py."""
    return "__init__" in answer


def _scan_cycles(sdk) -> int:
    """Linear naive scan: reveal files one at a time; return the cycle at which the hub is named."""
    seen: list[str] = []
    for cycle, rel in enumerate(NAIVE_ORDER, start=1):
        seen.append(f"# FILE: {rel}\n{(REPO / rel).read_text(encoding='utf-8')}")
        if _correct(_ask(sdk, f"Source files seen so far:\n\n{chr(10).join(seen)}\n\n{ASK}", "DebugScan")):
            return cycle
    return len(NAIVE_ORDER)


def _naive(sdk, ledger) -> dict:
    """Spec baseline: dump the whole repo (unfocused) for tokens/files; linear-scan cycles separately."""
    base = ledger.total_input()
    blob = "\n\n".join(f"# FILE: {f}\n{(REPO / f).read_text(encoding='utf-8')}" for f in NAIVE_ORDER)
    answer = _ask(sdk, f"FULL SOURCE of the repo:\n\n{blob}\n\n{ASK}", "DebugNaive")
    return {"input_tokens": ledger.total_input() - base, "files_read": len(NAIVE_ORDER),
            "iterations": _scan_cycles(sdk), "localized": _correct(answer), "answer": answer.strip()[:160]}


def _guided(sdk, ledger) -> dict:
    """Read the two graph-derived vault pages once (the suspects ranking routes straight to the hub)."""
    base = ledger.total_input()
    pages = [ROOT / "obsidian" / "index.md", ROOT / "obsidian" / "suspects.md"]
    ctx = "\n\n".join(p.read_text(encoding="utf-8") for p in pages)
    answer = _ask(sdk, f"Graph-derived vault context:\n\n{ctx}\n\n{ASK}", "DebugGuided")
    return {"input_tokens": ledger.total_input() - base, "files_read": len(pages),
            "iterations": 1, "localized": _correct(answer), "answer": answer.strip()[:160]}


def main() -> int:
    sdk = ArchLensSDK()
    ledger = sdk._gk().usage_ledger
    naive, guided = _naive(sdk, ledger), _guided(sdk, ledger)
    pct = lambda a, b: round((1 - b / a) * 100, 2) if a else 0.0  # noqa: E731
    result = {
        "task": "locate the file to fix first in andela/buggy-python (import failure)",
        "naive": naive, "graph_guided": guided,
        "token_savings_pct": pct(naive["input_tokens"], guided["input_tokens"]),
        "files_reduction_pct": pct(naive["files_read"], guided["files_read"]),
        "iteration_reduction": f"{guided['iterations']} vs {naive['iterations']} cycles",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"naive : {naive['input_tokens']} tok, {naive['files_read']} files, "
          f"{naive['iterations']} scan-cycles, correct={naive['localized']}")
    print(f"guided: {guided['input_tokens']} tok, {guided['files_read']} files, "
          f"{guided['iterations']} cycle, correct={guided['localized']}")
    print(f"tokens -{result['token_savings_pct']}% | files -{result['files_reduction_pct']}% | "
          f"cycles {result['iteration_reduction']}  ->  {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
