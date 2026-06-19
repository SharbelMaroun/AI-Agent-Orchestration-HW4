# Localization — produced by the BugLocalizer agent (EX04 §5.3)

This page is the **agent's** output, not hand-authored: `archlens` localizes the failing symbol
**graph-first** via `sdk.localize_bug(graph, "lambda_array")` (deterministic graph trace) and
`make_localizer_node` (the LangGraph node that then explains the root cause through the SDK LLM, given
**only the graph neighbourhood — no source code**). Code: `src/archlens/agents/bug_localizer.py`.

Run it yourself:

```bash
uv run python -c "from archlens.agents.bug_localizer import make_localizer_node; \
from archlens.sdk.sdk import ArchLensSDK; \
print(make_localizer_node(ArchLensSDK())({'graph_json':'artifacts/buggy-python-graph.json','failing_symbol':'lambda_array'}))"
```

## Agent output (on `artifacts/buggy-python-graph.json`)

- **Failing symbol:** `lambda_array`
- **Suspect (localized defect site):** `snippets_init` → **`snippets/__init__.py`** (the re-export hub)
- **Importers routing through the package:** `['main', 'snippets_init']`
- **Graph evidence (no source read):**
  - `lambda_array` resolves to node `snippets_loop_lambda_array`.
  - `main` imports it *through the package*, so the import is routed via the `snippets` hub.
  - Prime suspect `snippets_init` (degree 9 — the #1 centrality node) is the re-export hub every
    import must pass through, the natural origin of an `ImportError` for a package symbol.
- **Root cause (LLM, graph-first):** *"The file to fix is `snippets/__init__.py` … the central
  re-export hub all imports route through. The root cause is that it fails to import/expose
  `lambda_array` from `snippets_loop_lambda_array`, causing the ImportError when clients access it
  through the package."*

→ The deterministic trace + the LLM explanation agree: **fix the hub first** ([[repair#hub-snippetsinitpy]]),
then the gated leaf defects. See [[suspects]] for the full ranking and [[repair]] for the per-file fixes.
