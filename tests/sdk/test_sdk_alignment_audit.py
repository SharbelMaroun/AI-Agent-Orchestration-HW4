"""SDK-level test for the aggregated alignment audit (task 7.028)."""

from pathlib import Path

from archlens.sdk.sdk import ArchLensSDK

FIX = Path(__file__).resolve().parents[1] / "fixtures"
PRD = FIX / "prd_sample.md"
FULL = FIX / "graphify" / "full.json"


def test_alignment_audit_aggregates_all_sections():
    audit = ArchLensSDK().run_alignment_audit(PRD, FULL)
    for key in ("requirements", "matches", "gaps", "orphans", "shared_flows", "duplicate_flows"):
        assert key in audit
    assert len(audit["requirements"]) == 4


def test_alignment_audit_flags_gatekeeper_requirement_as_gap():
    audit = ArchLensSDK().run_alignment_audit(PRD, FULL)
    assert "NFR-01" in {g.req_id for g in audit["gaps"]}


def test_alignment_audit_reports_orphan_modules():
    audit = ArchLensSDK().run_alignment_audit(PRD, FULL)
    assert any(o.module == "auth_controller.py" for o in audit["orphans"])
