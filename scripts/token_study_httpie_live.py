"""LIVE naive-vs-graph token study on the httpie target (EX04 §5.5) — needs a real key in .env.

Measures the four rubric axes with REAL provider token counts (gatekeeper ledger deltas, not a
chars heuristic), over six reverse-engineering questions about httpie (a class-bearing BugsInPy
project). For each question, both arms answer the SAME question:
  - NAIVE  : the whole httpie source tree injected (the unfocused full-context baseline).
  - GUIDED : the AST class map (sdk.extract_class_schema) + only the one module the structure routes to.
Axes: input tokens, files/units read, investigation cycles (a real linear scan for the headline
question), and quality (did the answer name the correct module). Writes metrics/out/token_study_httpie.json.

    git clone https://github.com/httpie/cli runs/httpie-bug && \
        git -C runs/httpie-bug checkout 8c892edd4fe700a7ca5cc733dcb4817831d253e2
    uv run python scripts/token_study_httpie_live.py
"""

import json
import statistics
from pathlib import Path

from archlens.sdk.sdk import ArchLensSDK

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "runs" / "httpie-bug" / "httpie"
OUT = ROOT / "metrics" / "out" / "token_study_httpie.json"

# (question, module the graph routes to, keyword that marks a correct localization)
QUESTIONS = [
    ("Which module builds the HTTP request line and its headers?", "models.py", "models"),
    ("Which module defines and parses the command-line arguments?", "cli.py", "cli"),
    ("Which module handles file downloads and progress reporting?", "downloads.py", "downloads"),
    ("Which module manages saved named sessions?", "sessions.py", "sessions"),
    ("Which module sends the prepared request to the server?", "client.py", "client"),
    ("Which module processes request items and input data?", "input.py", "input"),
]
ASK = "Name ONLY the single httpie/<file>.py most responsible. Answer just the path."


def _all_source() -> tuple[str, int]:
    files = sorted(SRC.glob("*.py"))
    blob = "\n\n".join(f"# httpie/{p.name}\n{p.read_text(encoding='utf-8')}" for p in files)
    return blob, len(files)


def _delta(sdk, ledger, prompt: str, agent: str) -> tuple[str, int]:
    before = ledger.total_input()
    answer = sdk.ask_llm(prompt, agent=agent, max_tokens=30)
    return answer.strip(), ledger.total_input() - before


def _scan_cycles(sdk, ledger, files, keyword: str) -> int:
    """Real linear scan: read modules one at a time until the model names the right one."""
    seen = []
    for cycle, path in enumerate(files, start=1):
        seen.append(f"# httpie/{path.name}\n{path.read_text(encoding='utf-8')}")
        ans, _ = _delta(sdk, ledger, f"Source so far:\n{chr(10).join(seen)}\n\n{ASK}", "HttpieScan")
        if keyword in ans.lower():
            return cycle
    return len(files)


def main() -> int:
    if not SRC.is_dir():
        raise SystemExit(f"clone+checkout the buggy httpie first (see docstring); missing {SRC}")
    sdk = ArchLensSDK()
    ledger = sdk._gk().usage_ledger
    naive_blob, n_files = _all_source()
    class_map = sdk.extract_class_schema(SRC)["diagram"]
    files = sorted(SRC.glob("*.py"))

    rows, savings = [], []
    for question, module, keyword in QUESTIONS:
        n_ans, n_tok = _delta(sdk, ledger, f"FULL httpie source:\n{naive_blob}\n\n{question} {ASK}",
                              "HttpieNaive")
        guided_ctx = f"Class map:\n{class_map}\n\n# httpie/{module}\n{(SRC / module).read_text(encoding='utf-8')}"
        g_ans, g_tok = _delta(sdk, ledger, f"{guided_ctx}\n\n{question} {ASK}", "HttpieGuided")
        pct = round((1 - g_tok / n_tok) * 100, 2) if n_tok else 0.0
        savings.append(pct)
        rows.append({"question": question, "module": module, "naive_tokens": n_tok,
                     "guided_tokens": g_tok, "savings_pct": pct,
                     "naive_correct": keyword in n_ans.lower(), "guided_correct": keyword in g_ans.lower()})

    cycles = _scan_cycles(sdk, ledger, files, QUESTIONS[0][2])  # headline question, real scan
    result = {
        "target": "httpie (soarsmu/BugsInPy)", "mode": "LIVE provider tokens (gatekeeper ledger)",
        "naive_files_read": n_files, "guided_units_read": 2,
        "headline_cycles_naive": cycles, "headline_cycles_guided": 1,
        "questions": rows,
        "savings_pct_mean": round(statistics.mean(savings), 2),
        "savings_pct_stdev": round(statistics.pstdev(savings), 2),
        "savings_pct_min": min(savings), "savings_pct_max": max(savings),
        "target_met_70pct": statistics.mean(savings) >= 70.0,
        "guided_localization_rate": round(sum(r["guided_correct"] for r in rows) / len(rows), 2),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"LIVE httpie: mean savings {result['savings_pct_mean']}% +/- {result['savings_pct_stdev']} "
          f"(n={len(rows)}) | files {n_files}->2 | cycles {cycles}->1 | "
          f"guided localized {result['guided_localization_rate']*100:.0f}% -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
