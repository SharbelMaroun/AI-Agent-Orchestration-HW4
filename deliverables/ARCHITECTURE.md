# Architecture Report - andela/buggy-python

Version: 1.00 | Course: AI Agent Orchestration - HW4 / EX04

> **Provenance.** This document is a HAND-AUTHORED reverse-engineering synthesis, not raw generator
> output. Its facts are derived from machine-generated evidence: the auto-built graph
> `artifacts/buggy-python-graph.json` (19 nodes · 28 edges · 4 communities), its report
> `artifacts/buggy-python-GRAPH_REPORT.md`, and the `docs/diagrams/analysis_*.png` charts rendered by
> `scripts/visualize_graph.py`. ArchLens also ships a generic block-doc generator
> (`src/archlens/vault/arch_doc.py`, pinned by `tests/vault/test_arch_doc.py`) that emits a
> community-labelled `# Architecture` doc; this file instead presents a file-level, prose synthesis
> chosen for readability over that generic format. The OOP/class diagram below is intentionally empty
> because the target is procedural Python with no classes — see `deliverables/CLASS_SCHEMA.md`.

## Scope

This report describes the submitted target repository:

`https://github.com/andela/buggy-python`

Evidence:

- Graph: `artifacts/buggy-python-graph.json`
- Graph report: `artifacts/buggy-python-GRAPH_REPORT.md`
- Obsidian vault: `obsidian/`
- Bug report: `deliverables/BUG_REPORT.md`

## Graph Summary

| Metric | Value |
|---|---:|
| Nodes | 19 |
| Edges | 28 |
| Graphify communities | 4 |
| ArchLens density communities | 3 |
| Extraction evidence | 100% extracted |

## Block Diagram

```mermaid
flowchart TD
    main["main.py<br/>test harness"]
    init["snippets/__init__.py<br/>package re-export hub"]
    loop["snippets/loop.py<br/>lambda_array"]
    io["snippets/io.py<br/>loan JSON helpers"]
    foobar["snippets/foobar.py<br/>foo"]
    readme["README.md<br/>instructions"]

    main --> init
    init --> loop
    init --> io
    init --> foobar
    readme -.documents.-> main
```

## Main Architectural Finding

The project is small, but it has a clear cross-module dependency shape:

```text
entry point -> package hub -> leaf modules
```

The package hub, `snippets/__init__.py`, is the central architectural risk. Every import from
`main.py` passes through it, so missing re-exports can break the whole test harness before any leaf
module code is executed.

## Central Components

| Component | Role | Risk |
|---|---|---|
| `main.py` | Test harness / entry point | Cannot be modified; failures define expected behavior |
| `snippets/__init__.py` | Re-export hub | Single point for package imports; first bug site |
| `snippets/loop.py` | Lambda snippet | Contains JS-style Python mistakes |
| `snippets/io.py` | Loan calculation helpers | Contains dict-access, comparison, and typo bugs |
| `snippets/foobar.py` | Default-argument snippet | Contains mutable default argument bug |

## OOP View

This debugging target is procedural — functions and modules, no classes — so its own class schema is
honestly empty (`deliverables/CLASS_SCHEMA.md`). The §5.2 OOP class diagram (inheritance / composition
/ encapsulation) is therefore demonstrated on a class-bearing **secondary** reverse-engineering target,
**`deliverables/CLASS_SCHEMA_requests.md`** (psf/requests: 46 classes, 32 inheritance + 34 composition
edges, auto-extracted by the same AST pipeline).

```mermaid
classDiagram
```

## Reverse-Engineering Conclusion

The graph makes the bug easier to localize because it shows that the import failure is not primarily
inside `loop.py`; the failure must first pass through the package hub. That narrows the first repair
step to `snippets/__init__.py`, then guides the investigation into the gated leaf modules.
