# Target-Repository Selection (EX04 Core Task 1)

> Version: 1.01 | Status: Retargeted to PDF-listed repo | Course: AI Agent Orchestration - HW4 (EX04)

The project is now configured to use the assignment-listed BugsInPy repository as the
primary target. This removes the earlier risk that the analyzed repository was an
approved alternative rather than one of the PDF's named choices.

## 1. Current Selection

| Role | Repository | Branch | Pinned commit | Reason |
|---|---|---|---|---|
| Primary | `https://github.com/soarsmu/BugsInPy` | `master` | `11c5f1eea954a42132cfd06bf257766a7963e0fd` | PDF-listed EX04 target; real Python bug corpus |
| Fallback | `https://github.com/psf/requests` | `main` | config default | Simple, uv-friendly fallback if a target clone or validation step fails |

The primary target is configured in `config/setup.json` under `target_repo`.

## 2. Fresh Run Evidence

After clearing the LangGraph checkpoint, the pipeline cloned and analyzed BugsInPy:

```text
uv run python -c "from archlens.sdk.sdk import ArchLensSDK; sdk=ArchLensSDK(); sdk.reset_run_state(); print(sdk.analyze())"
```

Result:

```text
AnalysisReport(node_count=1639, edge_count=838, community_count=812,
               hubs=('readme', 'ansible_verify', 'ansible_verify_my_function',
                     '...cookiecutter_verify_sh__entry'),
               bottlenecks=('readme',), spofs=())
```

Generated artifacts:

| Artifact | Path |
|---|---|
| Graphify graph/report | `deliverables/graphify-out/` |
| Obsidian vault | `deliverables/bugsinpy-vault/` |
| Architecture/class/audit reports | `deliverables/ARCHITECTURE.md`, `deliverables/CLASS_SCHEMA.md`, `deliverables/ALIGNMENT_AUDIT.md` |

## 3. Historical Note

Earlier project evidence used `httpie/cli` as an approved BugsInPy-style target. That
work remains useful as development history, but the submission-facing configuration and
generated deliverables now use the PDF-listed `soarsmu/BugsInPy` repository.
