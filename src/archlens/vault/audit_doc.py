"""Generate deliverables/ALIGNMENT_AUDIT.md with four evidence-tagged sections (task 7.041)."""

from pathlib import Path

from archlens.graphops.flow_detector import detect_shared_flows
from archlens.graphops.gap_detector import detect_gaps
from archlens.graphops.orphan_detector import detect_orphans
from archlens.graphops.req_matcher import match_requirements
from archlens.graphops.req_parser import parse_requirements
from archlens.graphops.traceability import build_traceability
from archlens.graphops.verdicts import generate_verdicts
from archlens.shared.constants import ALIGNMENT_AUDIT_MD
from archlens.vault.evidence_lint import enforce_evidence


def render_audit(prd_source, graph_source, version: str) -> str:
    """Render the four audit sections; every claim carries exactly one evidence tag."""
    reqs = parse_requirements(prd_source)
    matches = match_requirements(reqs, graph_source)
    verdicts = generate_verdicts(build_traceability(matches, graph_source), graph_source)

    gaps = [f"{g.req_id}: {g.title} — searched {', '.join(g.searched)} [VALIDATED]."
            for g in detect_gaps(reqs, matches)]
    orphans = [f"{o.module} (degree {o.degree}) has no mapped requirement [EXTRACTED]."
               for o in detect_orphans(graph_source, matches)]
    flows = [f"{f.module} serves {', '.join(f.req_ids)} [INFERRED]."
             for f in detect_shared_flows(matches)]
    verdict_lines = [f"{v.text} [{'VALIDATED' if v.label == 'full traceability' else 'INFERRED'}]"
                     for v in verdicts]
    enforce_evidence(gaps + orphans + flows + verdict_lines)

    sections = [
        ("Unimplemented Requirements", gaps),
        ("Orphan Modules", orphans),
        ("Shared Flows", flows),
        ("Traceability Verdicts", verdict_lines),
    ]
    lines = ["# Alignment Audit", "", f"Version: {version}", ""]
    for title, claims in sections:
        body = [f"- {c}" for c in claims] if claims else ["- (none)"]
        lines += [f"## {title}", "", *body, ""]
    return "\n".join(lines).rstrip() + "\n"


def write_audit(prd_source, graph_source, out_dir, version: str) -> Path:
    """Write ALIGNMENT_AUDIT.md under out_dir and return its path."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / ALIGNMENT_AUDIT_MD
    path.write_text(render_audit(prd_source, graph_source, version), encoding="utf-8")
    return path
