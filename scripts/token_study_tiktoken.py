"""Rigorous token study with a REAL tokenizer (tiktoken) on a class-bearing, medium target (§5.5).

This addresses the small-repo / chars-heuristic / n=1 limits of the buggy-python debug study. It
measures REAL ``o200k_base`` (GPT-4.1 / 4o family) token counts of the NAIVE full-source context
versus a GRAPH-SCOPED context (the AST class-diagram structural map + the one focused module), across
SIX reverse-engineering questions over ``psf/requests``, and reports mean +/- std savings.

No live LLM is needed: this measures CONTEXT-WINDOW SIZE — the lecture's actual "inject every scale vs
retrieve a focused slice" claim — which is deterministic given a tokenizer. Writes
``metrics/out/token_study_requests.json``.

    git clone --depth 1 https://github.com/psf/requests runs/requests
    uv run python scripts/token_study_tiktoken.py
"""

import json
import statistics
from pathlib import Path

import tiktoken

from archlens.sdk.sdk import ArchLensSDK

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "runs" / "requests" / "src" / "requests"
OUT = ROOT / "metrics" / "out" / "token_study_requests.json"
ENCODING = "o200k_base"  # GPT-4.1 / 4o family tokenizer

# Reverse-engineering questions -> the focused module the graph routes to (deterministic mapping).
QUESTIONS = [
    ("How is HTTP authentication implemented?", "auth.py"),
    ("What is the exception hierarchy?", "exceptions.py"),
    ("How does the HTTPAdapter manage connection pooling and retries?", "adapters.py"),
    ("How is a request prepared and sent?", "models.py"),
    ("How does a Session persist state across requests?", "sessions.py"),
    ("How are cookies stored and merged?", "cookies.py"),
]


def _naive_context(enc) -> int:
    """Naive baseline: inject the entire source tree (the lecture's unfocused context)."""
    blob = "\n\n".join(f"# {p.name}\n{p.read_text(encoding='utf-8')}"
                       for p in sorted(SRC.glob("*.py")))
    return len(enc.encode(blob))


def _guided_context(enc, structural_map: str, module: str) -> int:
    """Graph-scoped retrieval: the structural class map + only the one focused module."""
    focused = (SRC / module).read_text(encoding="utf-8")
    return len(enc.encode(f"{structural_map}\n\n# {module}\n{focused}"))


def main() -> int:
    if not SRC.is_dir():
        raise SystemExit("clone the target first: git clone --depth 1 "
                         f"https://github.com/psf/requests runs/requests  (missing {SRC})")
    enc = tiktoken.get_encoding(ENCODING)
    structural_map = ArchLensSDK().extract_class_schema(SRC)["diagram"]
    naive_tokens = _naive_context(enc)

    rows, savings = [], []
    for question, module in QUESTIONS:
        guided_tokens = _guided_context(enc, structural_map, module)
        pct = round((1 - guided_tokens / naive_tokens) * 100, 2)
        savings.append(pct)
        rows.append({"question": question, "focused_module": module,
                     "naive_tokens": naive_tokens, "guided_tokens": guided_tokens,
                     "savings_pct": pct})

    result = {
        "target": "psf/requests",
        "tokenizer": f"tiktoken {ENCODING} (real tokens, not a chars heuristic)",
        "measures": "input context-window size (naive full-source dump vs graph-scoped retrieval)",
        "modules_in_target": len(list(SRC.glob("*.py"))),
        "naive_tokens": naive_tokens,
        "questions": rows,
        "savings_pct_mean": round(statistics.mean(savings), 2),
        "savings_pct_stdev": round(statistics.pstdev(savings), 2),
        "savings_pct_min": min(savings),
        "savings_pct_max": max(savings),
        "target_met_70pct": statistics.mean(savings) >= 70.0,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"naive {naive_tokens} tok | guided mean savings {result['savings_pct_mean']}% "
          f"+/- {result['savings_pct_stdev']} (n={len(rows)}, range "
          f"{result['savings_pct_min']}-{result['savings_pct_max']}%) -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
