from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional, Tuple
from uuid import uuid4


# ==========================================================
# Evidence
# ==========================================================

@dataclass(frozen=True, slots=True)
class Evidence:
    """
    A single piece of evidence supporting a Reason.
    """

    name: str
    value: Any
    source: Optional[str] = None


# ==========================================================
# Reason
# ==========================================================

@dataclass(frozen=True, slots=True)
class Reason:
    """
    Explainable reason supporting the recommended action.
    """

    title: str
    description: str = ""
    evidence: Tuple[Evidence, ...] = ()


# ==========================================================
# Decision Context
# ==========================================================

@dataclass(frozen=True, slots=True)
class DecisionContext:
    """
    Market context at decision time.
    """

    trend: Optional[str] = None
    market_bias: Optional[str] = None
    risk: Optional[str] = None


# ==========================================================
# Decision Metadata
# ==========================================================

@dataclass(frozen=True, slots=True)
class DecisionMetadata:
    """
    Technical metadata attached to a Decision Artifact.
    """

    engine_version: str

    symbol: str

    pair: str

    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    signal_version: Optional[str] = None

    interpretation_version: Optional[str] = None

    chain: Optional[str] = None


# ==========================================================
# Decision Artifact
# ==========================================================

@dataclass(frozen=True, slots=True)
class DecisionArtifact:
    """
    Official output produced by the Decision Engine.

    Architecture Notes
    ------------------
    - Immutable
    - Explainable
    - Evidence-Based
    - No business logic
    - No validation
    - Validation handled by Decision Gate
    """

    recommended_action: str

    confidence: int

    summary: str

    context: DecisionContext

    reasons: Tuple[Reason, ...]

    metadata: DecisionMetadata

    artifact_id: str = field(
        default_factory=lambda: f"DEC-{uuid4().hex[:12].upper()}"
    )