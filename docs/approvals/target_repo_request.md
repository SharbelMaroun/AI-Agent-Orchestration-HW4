# Target-Repository Approval Request

> Version: 1.00 | Status: Sent and approved 2026-06-14 | Course: AI Agent Orchestration — HW4 (EX04)

**Prepared:** 2026-06-13 (sent-date to be stamped on dispatch)
**To:** Course lecturer
**From:** Sharbel Maroun
**Subject:** EX04 target-repository approval (L07 §11 Core Task 1)

Per L07 §11, the target repository requires lecturer approval. The shortlist below is
detailed in `docs/PRD.md`, Appendix B (selection criteria included).

| # | Candidate | Type | Why |
|---|---|---|---|
| 1 | https://github.com/soarsmu/BugsInPy | PDF-listed repository | Official assignment option; registry of real Python bugs used for reverse-engineering and debugging |
| 2 | https://github.com/tqdm/tqdm | BugsInPy project | Small; `uv sync` fails on a dep conflict but `--with-editable` works (evidence in docs/REPO_SELECTION.md) |
| 3 | https://github.com/nvbn/thefuck | BugsInPy project | Pure Python, plugin architecture interesting for graph analysis; setup.py-only |
| F | https://github.com/psf/requests | Simpler fallback | Well-tested, moderate size — the L07 §11.2 "don't get stuck" fallback |

**Requested decision:** use candidate #1 (BugsInPy) as primary with F (requests) as
the documented fallback. Full measured evidence:
docs/REPO_SELECTION.md.

Approval will be recorded in `docs/approvals/target_repo_approval.md` (TODO 2.010).
