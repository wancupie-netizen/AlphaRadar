from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from core.artifacts.decision_artifact import DecisionArtifact
from core.models.market_snapshot import MarketSnapshot


@dataclass(frozen=True, slots=True)
class OutcomeArtifact:
    """
    Official output produced by the Outcome Recording Engine.

    Architecture Notes
    ------------------
    - Immutable
    - Contains no business logic
    - Contains no evaluation
    - Contains no learning
    - Contains no validation

    Purpose
    -------
    Records market reality after a DecisionArtifact has been created.
    """

    decision_artifact_id: str

    observation_window: str

    market_snapshot: MarketSnapshot

    snapshot_status: str

    artifact_id: str = field(
        default_factory=lambda: f"OUT-{uuid4().hex[:12].upper()}"
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @classmethod
    def from_decision(
        cls,
        decision: DecisionArtifact,
        market_snapshot: MarketSnapshot,
        observation_window: str,
        snapshot_status: str = "RECORDED",
    ) -> "OutcomeArtifact":
        """
        Convenience factory that links an OutcomeArtifact
        to an existing DecisionArtifact.
        """

        return cls(

            decision_artifact_id=decision.artifact_id,

            observation_window=observation_window,

            market_snapshot=market_snapshot,

            snapshot_status=snapshot_status,

        )