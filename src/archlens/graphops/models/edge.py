"""Edge model with confidence-range validation; relation is an open AST vocabulary (4.025-4.026).

Graphify emits an open relation set (calls, contains, imports_from, inherits, re_exports,
references, method, ...), so `relation` is a free string rather than a closed enum.
"""

from pydantic import BaseModel, ConfigDict, Field, model_validator

from archlens.shared.constants import (
    CONFIDENCE_MAX,
    CONFIDENCE_MIN,
    EXTRACTED_CONFIDENCE,
    EvidenceType,
)


class Edge(BaseModel):
    """A directed, evidence-typed edge; reading order is relation -> confidence -> source_file."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    src: str = Field(alias="from")
    dst: str = Field(alias="to")
    relation: str
    type: EvidenceType
    confidence: float
    source_file: str

    @model_validator(mode="after")
    def _check_confidence(self) -> "Edge":
        if not CONFIDENCE_MIN <= self.confidence <= CONFIDENCE_MAX:
            raise ValueError(
                f"confidence {self.confidence} outside [{CONFIDENCE_MIN}, {CONFIDENCE_MAX}]"
            )
        if self.type is EvidenceType.EXTRACTED and self.confidence != EXTRACTED_CONFIDENCE:
            raise ValueError(f"EXTRACTED edges must be pinned at {EXTRACTED_CONFIDENCE}")
        return self
