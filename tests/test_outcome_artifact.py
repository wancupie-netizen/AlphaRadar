from decimal import Decimal

from core.artifacts.decision_artifact import (
    DecisionArtifact,
    DecisionContext,
    DecisionMetadata,
)

from core.artifacts.outcome_artifact import (
    OutcomeArtifact,
)

from core.models.market_snapshot import (
    MarketSnapshot,
)

print("=" * 60)
print("Outcome Artifact Test")
print("=" * 60)

# --------------------------------------------------
# Decision
# --------------------------------------------------

decision = DecisionArtifact(

    recommended_action="WATCH",

    confidence="HIGH",

    summary="Outcome Test",

    context=DecisionContext(),

    reasons=(),

    metadata=DecisionMetadata(

        engine_version="1.0.0",

        symbol="BTC",

        pair="BTC/USDT",

    ),

)

# --------------------------------------------------
# Market Snapshot
# --------------------------------------------------

snapshot = MarketSnapshot(

    symbol="BTC",

    pair="BTC/USDT",

    chain="solana",

    price=Decimal("80000"),

    liquidity=Decimal("5000000"),

    volume_24h=Decimal("1200000"),

)

# --------------------------------------------------
# Outcome
# --------------------------------------------------

outcome = OutcomeArtifact.from_decision(

    decision=decision,

    market_snapshot=snapshot,

    observation_window="24H",

)

print(outcome)

# --------------------------------------------------
# Assertions
# --------------------------------------------------

assert outcome.decision_artifact_id == decision.artifact_id

assert outcome.created_at is not None

assert outcome.market_snapshot.symbol == "BTC"

assert outcome.snapshot_status == "RECORDED"

print("\nPASS")