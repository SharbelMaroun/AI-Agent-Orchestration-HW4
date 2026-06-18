# Target Repo Request

**Course:** AI Agent Orchestration HW4 / EX04  
**Status:** Final single-target selection

## Candidate

| Candidate | Type | Why |
|---|---|---|
| `https://github.com/andela/buggy-python` | PDF-listed repository | Small runnable debugging corpus; pure Python; clear failing `main.py` harness; supports graph-first localization and repair evidence |

## Decision

Use `andela/buggy-python` as the single EX04 target repository. The full submission story is:

1. Build/read the graph artifact in `artifacts/buggy-python-graph.json`.
2. Navigate the investigation through the Obsidian vault in `obsidian/`.
3. Use `BugLocalizer` to identify the re-export hub defect.
4. Document the code fix and failing-to-passing verification in `deliverables/BUG_REPORT.md`.
