"""TDD tests for the ALIGNMENT_AUDIT.md generator (tasks 7.040-7.041)."""

from pathlib import Path

from archlens.vault.audit_doc import render_audit, write_audit

FIX = Path(__file__).resolve().parents[1] / "fixtures"
PRD = FIX / "prd_sample.md"
FULL = FIX / "graphify" / "full.json"


def test_has_all_four_section_headings():
    text = render_audit(PRD, FULL, "1.00")
    for heading in ("## Unimplemented Requirements", "## Orphan Modules",
                    "## Shared Flows", "## Traceability Verdicts"):
        assert heading in text


def test_lists_the_gatekeeper_gap():
    assert "NFR-01" in render_audit(PRD, FULL, "1.00")


def test_every_claim_carries_an_evidence_tag():
    claims = [ln for ln in render_audit(PRD, FULL, "1.00").splitlines()
              if ln.startswith("- ") and ln != "- (none)"]
    tags = ("OBSERVED", "INFERRED", "EXTRACTED", "VALIDATED")
    assert claims
    assert all(any(t in c for t in tags) for c in claims)


def test_write_produces_audit_file(tmp_path):
    path = write_audit(PRD, FULL, tmp_path, "1.00")
    assert path.name == "ALIGNMENT_AUDIT.md"
    assert "## Shared Flows" in path.read_text(encoding="utf-8")
