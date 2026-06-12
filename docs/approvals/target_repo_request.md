# Target-Repository Approval Request

> Version: 1.00 | Status: Prepared — pending send/approval | Course: AI Agent Orchestration — HW4 (EX04)

**Prepared:** 2026-06-13 (sent-date to be stamped on dispatch)
**To:** Course lecturer
**From:** Sharbel Maroun
**Subject:** EX04 target-repository approval (L07 §11 Core Task 1)

Per L07 §11, the target repository requires lecturer approval. The shortlist below is
detailed in `docs/PRD.md`, Appendix B (selection criteria included).

| # | Candidate | Type | Why |
|---|---|---|---|
| 1 | https://github.com/tqdm/tqdm | BugsInPy project | Pure Python, small, real BugsInPy bug history, pytest suite, uv-compatible |
| 2 | https://github.com/httpie/cli | BugsInPy project | Pure Python, moderate size, active pytest suite |
| 3 | https://github.com/nvbn/thefuck | BugsInPy project | Pure Python, plugin architecture interesting for graph analysis |
| F | https://github.com/psf/requests | Simpler fallback | Well-tested, moderate size — the L07 §11.2 "don't get stuck" fallback |

**Requested decision:** approve candidate #1 (tqdm) as primary with F (requests) as
the documented fallback, or indicate a preferred alternative.

Approval will be recorded in `docs/approvals/target_repo_approval.md` (TODO 2.010).
