from decimal import Decimal

from core.artifacts.decision_artifact import (
    DecisionArtifact,
    DecisionContext,
    DecisionMetadata,
)

from core.artifacts.outcome_artifact import (
    OutcomeArtifact,
)

from core.artifacts.learning_artifact import (
    LearningArtifact,
)

from core.models.market_snapshot import (
    MarketSnapshot,
)

print("=" * 60)
print("Learning Artifact Test")
print("=" * 60)

decision = DecisionArtifact(

    recommended_action="WATCH",

    confidence="HIGH",

    summary="Learning Test",

    context=DecisionContext(),

    reasons=(),

    metadata=DecisionMetadata(

        engine_version="1.0.0",

        symbol="BTC",

        pair="BTC/USDT",

    ),

)

snapshot = MarketSnapshot(

    symbol="BTC",

    pair="BTC/USDT",

    chain="solana",

    price=Decimal("80000"),

    liquidity=Decimal("5000000"),

    volume_24h=Decimal("1200000"),

)

outcome = OutcomeArtifact.from_decision(

    decision=decision,

    market_snapshot=snapshot,

    observation_window="24H",

)

learning = LearningArtifact.from_outcome(

    outcome=outcome,

    learning_status="PENDING",

    summary="Initial learning",

)

print(learning)

assert learning.token == "BTC"

assert learning.outcome_artifact_id == outcome.artifact_id

assert learning.learning_status == "PENDING"

assert learning.created_at is not None

print("\nPASS")