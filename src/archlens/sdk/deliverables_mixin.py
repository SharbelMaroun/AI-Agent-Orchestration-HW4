"""Phase 7 reverse-engineering deliverable methods, mixed into ArchLensSDK."""

from ..graphops.block_model import build_block_model
from ..graphops.class_extractor import extract_classes
from ..graphops.class_relations import class_relations
from ..graphops.flow_detector import detect_duplicate_flows, detect_shared_flows
from ..graphops.gap_detector import detect_gaps
from ..graphops.mermaid_blocks import render_block_diagram
from ..graphops.mermaid_classes import render_class_diagram
from ..graphops.orphan_detector import detect_orphans
from ..graphops.req_matcher import match_requirements
from ..graphops.req_parser import parse_requirements
from ..vault.arch_doc import write_architecture
from ..vault.audit_doc import write_audit
from ..vault.class_doc import write_class_schema


class DeliverablesMixin:
    """Single-entry SDK methods that render reverse-engineering deliverables."""

    def generate_block_diagram(self, graph_source, direction: str | None = None) -> str:
        """Render the architecture block diagram (mermaid flowchart) from a graph.json."""
        direction = direction or self._config().deliverables.mermaid_direction
        return render_block_diagram(build_block_model(graph_source), direction)

    def extract_class_schema(self, source_root) -> dict:
        """Extract the OOP class model and render it as a mermaid classDiagram."""
        classes = extract_classes(source_root)
        relations = class_relations(source_root)
        return {
            "classes": classes,
            "relations": relations,
            "diagram": render_class_diagram(classes, relations),
        }

    def run_alignment_audit(self, prd_source, graph_source) -> dict:
        """Aggregate requirement gaps, orphan modules, and shared/duplicate flows into one audit."""
        requirements = parse_requirements(prd_source)
        matches = match_requirements(requirements, graph_source)
        return {
            "requirements": requirements,
            "matches": matches,
            "gaps": detect_gaps(requirements, matches),
            "orphans": detect_orphans(graph_source, matches),
            "shared_flows": detect_shared_flows(matches),
            "duplicate_flows": detect_duplicate_flows(graph_source),
        }

    def generate_deliverables(self, graph_source, source_root, prd_source,
                              out_dir=None, version: str | None = None) -> list:
        """Write ARCHITECTURE.md, CLASS_SCHEMA.md, and ALIGNMENT_AUDIT.md; return their paths."""
        version = version or self.version()
        out_dir = out_dir or self._config().deliverables.output_dir
        direction = self._config().deliverables.mermaid_direction
        return [
            write_architecture(graph_source, out_dir, version, direction),
            write_class_schema(source_root, out_dir, version),
            write_audit(prd_source, graph_source, out_dir, version),
        ]
