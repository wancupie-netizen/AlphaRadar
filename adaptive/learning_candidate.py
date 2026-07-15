from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from collections.abc import Mapping
from typing import Any

from experience_memory import Experience


@dataclass(frozen=True)
class LearningCandidate:
    """
    Immutable learning candidate generated
    from an Experience.

    This object is the bridge between the
    Memory Subsystem and the future
    Learning Subsystem.
    """

    experience: Experience

    decision_id: str

    decision_fingerprint: str

    market_dna: str

    decision: str

    confidence: float

    metadata: Mapping[str, Any]


class LearningCandidateBuilder:
    """
    Build immutable LearningCandidate objects.

    Current implementation performs no
    learning, filtering or scoring.

    Future implementations may validate
    completed trade outcomes before
    producing candidates.
    """

    def build(
        self,
        experience: Experience,
    ) -> LearningCandidate:

        metadata = MappingProxyType(
            dict(experience.metadata)
        )

        return LearningCandidate(
            experience=experience,

            decision_id=experience.decision_id,

            decision_fingerprint=experience.decision_fingerprint,

            market_dna=experience.market_dna,

            decision=experience.decision,

            confidence=experience.confidence,

            metadata=metadata,
        )