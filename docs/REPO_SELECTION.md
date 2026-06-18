# Target-Repository Selection (EX04 Core Task 1)

> Version: 1.02 | Status: Merge-resolved | Course: AI Agent Orchestration - HW4 (EX04)

The active configured target remains the PDF-listed **BugsInPy** repository, matching the retargeting
decision made before this merge. The partner branch also adds a supplemental debugging track for
**andela/buggy-python**, another PDF-listed corpus.

- `config/setup.json` primary target: `https://github.com/soarsmu/BugsInPy`
- BugsInPy reverse-engineering artifacts: `deliverables/graphify-out/` and `deliverables/bugsinpy-vault/`
- Supplemental buggy-python evidence: `deliverables/BUG_REPORT.md`, `artifacts/buggy-python-graph.json`,
  and the focused `obsidian/` investigation vault

## 1. Current Selection

| Role | Repository | Branch | Pinned commit | Reason |
|---|---|---|---|---|
| Primary | `https://github.com/soarsmu/BugsInPy` | `master` | `11c5f1eea954a42132cfd06bf257766a7963e0fd` | PDF-listed EX04 target; real Python bug corpus |
| Fallback | `https://github.com/psf/requests` | `main` | config default | Simple, uv-friendly fallback if a target clone or validation step fails |
| Supplemental debugging subject | `https://github.com/andela/buggy-python` | `master` | partner artifact | PDF-listed small debugging corpus with concrete bug-localization evidence |

## 2. Fresh BugsInPy Run Evidence

```text
AnalysisReport(node_count=1639, edge_count=838, community_count=812,
               hubs=('readme', 'ansible_verify', 'ansible_verify_my_function',
                     '...cookiecutter_verify_sh__entry'),
               bottlenecks=('readme',), spofs=())
```

## 3. Generated Artifacts

| Artifact | Path |
|---|---|
| BugsInPy Graphify graph/report | `deliverables/graphify-out/` |
| BugsInPy Obsidian vault | `deliverables/bugsinpy-vault/` |
| Reverse-engineering reports | `deliverables/ARCHITECTURE.md`, `deliverables/CLASS_SCHEMA.md`, `deliverables/ALIGNMENT_AUDIT.md` |
| Supplemental buggy-python bug report | `deliverables/BUG_REPORT.md` |

## 4. Historical Note

Earlier project evidence used `httpie/cli` as an approved scale target for the token-economics study.
That work remains development history, but the active configured EX04 target is BugsInPy.
