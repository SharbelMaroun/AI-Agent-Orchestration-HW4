<!-- ArchLens pull-request template (task 16.013). Tick every box before requesting review. -->

## Summary

<!-- What does this PR change, and why? Reference task IDs where helpful. -->

## Quality gate checklist

- [ ] Tests green (`uv run pytest`)
- [ ] Coverage >= 85% (`uv run pytest --cov=src/archlens --cov-branch`)
- [ ] Ruff reports 0 violations (`uv run ruff check .`)
- [ ] 150-line cap holds (`uv run python scripts/check_line_cap.py`)
- [ ] No secrets committed (gitleaks clean; `.env` git-ignored)
- [ ] Docs updated (README / PRD / TODO as applicable)
