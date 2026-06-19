# Token Study - psf/requests (rigorous, real tokenizer)

Version: 1.00 | Course: AI Agent Orchestration - HW4 (EX04)

This is the submission's **scale** token-efficiency study, complementing the conservative focused
debug-localization study on the tiny `andela/buggy-python` target (14.59%, `debug_token_study.json`).
It answers the limitations a strict reading raises about a 5-file target: it uses a **real tokenizer**
(not a `chars//4` heuristic), a **medium real-world class-bearing repo** (`psf/requests`, 19 modules),
and **six questions** so savings carry a measured variance rather than a single n=1 point.

- Source / artifact: `scripts/token_study_tiktoken.py` -> `metrics/out/token_study_requests.json`
- Tokenizer: `tiktoken o200k_base` (GPT-4.1 / 4o family) — counts of the actual context strings.
- What is measured: **input context-window size**, i.e. the lecture's core claim — naive injects every
  scale into the window, graph-scoped retrieval injects a focused slice. No live LLM is required
  because context size is deterministic given a tokenizer.

## Method

- **Naive baseline (per question):** inject the entire source tree (all 19 modules) — the lecture's
  unfocused "all scales in the window" context. **49,592 real tokens.**
- **Graph-scoped (per question):** the AST class-diagram structural map (~1.8k tokens, the same
  `sdk.extract_class_schema` used for the §5.2 OOP diagram) **plus only the one module the structure
  routes the question to**.

## Results (n = 6 questions)

| Question | Focused module | Naive tok | Guided tok | Savings |
|---|---|---:|---:|---:|
| HTTP authentication | `auth.py` | 49592 | (map+module) | **90.50%** |
| Exception hierarchy | `exceptions.py` | 49592 | (map+module) | **94.38%** |
| HTTPAdapter pooling/retries | `adapters.py` | 49592 | (map+module) | **84.25%** |
| Request preparation/sending | `models.py` | 49592 | (map+module) | **77.89%** |
| Session state | `sessions.py` | 49592 | (map+module) | **81.41%** |
| Cookie storage/merge | `cookies.py` | 49592 | (map+module) | **86.35%** |

**Mean savings: 85.80% +/- 5.48% (std), range 77.89%-94.38% — clears the lecture's 70% target.**

## Honesty notes

- The naive baseline is the lecture's own "inject every scale" full-context scenario, not an invented
  strawman; on a real medium repo this is exactly the context-bloat the graph approach targets.
- This measures **input context size**, the dominant cost the lecture addresses; it does not model
  output tokens or a multi-turn agent loop.
- The two studies are complementary: `buggy-python` is the conservative floor (tiny repo, 14.59%);
  `requests` is the scale result (medium repo, ~86%). Neither is blended into the other.
