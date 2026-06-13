"""Centralized named constants — the only sanctioned home for magic values."""

from enum import Enum
from pathlib import Path

CONFIG_DIR = Path("config")
SETUP_FILE = CONFIG_DIR / "setup.json"
RATE_LIMITS_FILE = CONFIG_DIR / "rate_limits.json"
LOGGING_CONFIG_FILE = CONFIG_DIR / "logging_config.json"

LINE_CAP = 150
MAX_LOOP_ITERATIONS = 5

LOGGER_NAME = "archlens"

# Repo-module constants (task 3.014)
ALLOWED_URL_SCHEMES = ("https",)
DEFAULT_CLONE_DEPTH = 1
DEFAULT_TIMEOUT_S = 300
DEFAULT_MAX_SIZE_MB = 200

# Graphify pipeline constants (Phase 4)
GRAPH_JSON = "graph.json"
GRAPH_HTML = "graph.html"
REPORT_MD = "REPORT.md"
MANIFEST_JSON = "manifest.json"
GRAPHIFY_STAGES = ("detect", "extract", "build", "cluster", "export")
ANALYSIS_DEPTHS = ("structural", "semantic", "full")
CONFIDENCE_MIN = 0.55
CONFIDENCE_MAX = 0.95
EXTRACTED_CONFIDENCE = 0.95
DUPLICATE_SIMILARITY_THRESHOLD = 0.91
LOW_CONFIDENCE_FLOOR = 0.65

# Obsidian vault constants (Phase 5)
HOT_MD = "hot.md"
INDEX_MD = "index.md"
LOG_MD = "log.md"
RAW_DIR = "raw"
WIKI_DIR = "wiki"
FRONTMATTER_KEYS = ("type", "status", "project")
HOT_MAX_LINES = 120

# Phase 7 reverse-engineering deliverables
DELIVERABLES_DIR = "deliverables"
ARCHITECTURE_MD = "ARCHITECTURE.md"
CLASS_SCHEMA_MD = "CLASS_SCHEMA.md"
ALIGNMENT_AUDIT_MD = "ALIGNMENT_AUDIT.md"
EVIDENCE_TAGS = ("OBSERVED", "INFERRED", "EXTRACTED", "VALIDATED")


class NodeType(str, Enum):
    """graph.json node kinds (PRD_graph_pipeline §4.1)."""

    CODE = "code"
    DOC = "doc"
    TEST = "test"
    RATIONALE = "rationale"
    MEDIA = "media"
    CONFIG = "config"


class EvidenceType(str, Enum):
    """Edge certainty levels — the evidence ladder (Part C p6)."""

    EXTRACTED = "EXTRACTED"
    INFERRED = "INFERRED"
    AMBIGUOUS = "AMBIGUOUS"


class Relation(str, Enum):
    """Closed relation vocabulary (PRD_graph_pipeline §4.2)."""

    IMPLEMENTS = "implements"
    IMPORTS = "imports"
    CALLS = "calls"
    USES = "uses"
    MENTIONS = "mentions"
    TESTED_BY = "tested_by"
    RATIONALE_FOR = "rationale_for"
    SEMANTICALLY_SIMILAR_TO = "semantically_similar_to"
    VALIDATES = "validates"
    WRITES_SESSION = "writes_session"
    CHECKS_POLICY = "checks_policy"
    READS = "reads"
    DEFINES = "defines"
    AMBIGUOUS = "ambiguous"


class RationaleSubtype(str, Enum):
    """Rationale-node subtypes (Part C p15)."""

    WHY = "WHY"
    TODO = "TODO"
    NOTE = "NOTE"


class CriticalRelation(str, Enum):
    """Security-critical relations whose chains define SPOF paths (task 6.027, Part C)."""

    VALIDATES = "validates"
    WRITES_SESSION = "writes_session"
    CHECKS_POLICY = "checks_policy"
