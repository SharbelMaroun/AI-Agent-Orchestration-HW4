# ArchLens

Multi-agent, graph-based reverse engineering of Python codebases — HW4/EX04 for the
AI Agent Orchestration course. ArchLens clones a target repository, builds a knowledge
graph with Graphify, navigates it in an Obsidian vault, detects architectural defects
with LangGraph agents, fixes them in a measured improvement loop, and proves token savings.

Full documentation lives in `docs/` (PRD, PLAN, specialized PRDs, TODO, prompt book).

## Quickstart (uv only)

```bash
uv sync                          # install the locked environment
uv run pytest                    # run the test suite (coverage gate: 85%)
uv run ruff check .              # lint gate: zero violations
uv run python src/main.py --version
```

All tooling goes through uv; this project never uses other package managers.
