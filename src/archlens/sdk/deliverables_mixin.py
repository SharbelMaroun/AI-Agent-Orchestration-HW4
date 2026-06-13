"""Phase 7 reverse-engineering deliverable methods, mixed into ArchLensSDK."""

from archlens.graphops.block_model import build_block_model
from archlens.graphops.class_extractor import extract_classes
from archlens.graphops.class_relations import class_relations
from archlens.graphops.flow_detector import detect_duplicate_flows, detect_shared_flows
from archlens.graphops.gap_detector import detect_gaps
from archlens.graphops.mermaid_blocks import render_block_diagram
from archlens.graphops.mermaid_classes import render_class_diagram
from archlens.graphops.orphan_detector import detect_orphans
from archlens.graphops.req_matcher import match_requirements
from archlens.graphops.req_parser import parse_requirements


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
