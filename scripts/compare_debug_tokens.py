"""Token study for the EX04 debugging task: naive raw-file reading vs graph-guided context.

Asks the SAME question ("which file holds the bug and what is the root cause?") two ways over the
andela/buggy-python clone: (1) NAIVE — stuff the full source of every module; (2) GRAPH-GUIDED —
read only the graph-derived vault pages (index + suspects). Real input tokens come from the
gatekeeper ledger. Writes metrics/out/debug_token_study.json. Needs a live key in .env.

    uv run python scripts/compare_debug_tokens.py
"""

import json
from pathlib import Path

from archlens.sdk.sdk import ArchLensSDK

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT / "runs" / "buggy-python"
OUT = ROOT / "metrics" / "out" / "debug_token_study.json"
QUESTION = ("You are debugging this Python repository whose test harness main.py fails. In 3-4 "
            "sentences, name the file(s) that contain the bug and explain the root cause.")


def _source_files() -> list[Path]:
    return sorted(p for p in REPO.glob("**/*.py") if ".git" not in p.parts)


def _naive_context() -> tuple[str, int]:
    files = _source_files()
    blob = "\n\n".join(f"# FILE: {p.relative_to(REPO)}\n{p.read_text(encoding='utf-8')}" for p in files)
    return blob, len(files)


def _guided_context() -> tuple[str, int]:
    pages = [ROOT / "obsidian" / "index.md", ROOT / "obsidian" / "suspects.md"]
    blob = "\n\n".join(p.read_text(encoding="utf-8") for p in pages)
    return blob, len(pages)


def main() -> int:
    sdk = ArchLensSDK()
    ledger = sdk._gk().usage_ledger
    naive_ctx, naive_files = _naive_context()
    guided_ctx, guided_files = _guided_context()

    before = ledger.total_input()
    sdk.ask_llm(f"{QUESTION}\n\nFULL SOURCE:\n{naive_ctx}", agent="DebugNaive", max_tokens=300)
    naive_tokens = ledger.total_input() - before

    before = ledger.total_input()
    sdk.ask_llm(f"{QUESTION}\n\nGRAPH-GUIDED CONTEXT (vault index + suspects):\n{guided_ctx}",
                agent="DebugGuided", max_tokens=300)
    guided_tokens = ledger.total_input() - before

    savings = round((1 - guided_tokens / naive_tokens) * 100, 2) if naive_tokens else 0.0
    result = {
        "task": "locate the bug + root cause in andela/buggy-python",
        "naive": {"input_tokens": naive_tokens, "files_read": naive_files},
        "graph_guided": {"input_tokens": guided_tokens, "files_read": guided_files},
        "token_savings_pct": savings,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"naive: {naive_tokens} input tokens over {naive_files} files")
    print(f"graph-guided: {guided_tokens} input tokens over {guided_files} files")
    print(f"token savings: {savings}%   ->  {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
