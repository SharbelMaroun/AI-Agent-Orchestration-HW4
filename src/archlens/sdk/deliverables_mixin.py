"""Phase 7 reverse-engineering deliverable methods, mixed into ArchLensSDK."""

from archlens.graphops.block_model import build_block_model
from archlens.graphops.class_extractor import extract_classes
from archlens.graphops.class_relations import class_relations
from archlens.graphops.mermaid_blocks import render_block_diagram
from archlens.graphops.mermaid_classes import render_class_diagram


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
