"""
Lifecycle Engine Test
"""

from decimal import Decimal
from pprint import pprint

from core.artifacts.decision_artifact import (
    DecisionArtifact,
    DecisionContext,
    DecisionMetadata,
)

from core.models.market_snapshot import (
    MarketSnapshot,
)

from scanner.lifecycle_engine import (
    build_lifecycle,
)


print("=" * 60)
print("Lifecycle Engine Test")
print("=" * 60)


decision = DecisionArtifact(

    recommended_action="WATCH",

    confidence="HIGH",

    summary="Lifecycle Test",

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


package = build_lifecycle(

    decision=decision,

    market_snapshot=snapshot,

    observation_window="24H",

)

pprint(package)

assert package["decision"] is decision

assert package["gate"].status == "APPROVED"

assert package["outcome"].decision_artifact_id == decision.artifact_id

assert package["learning"].outcome_artifact_id == package["outcome"].artifact_id

assert package["knowledge"].learning_artifact_id == package["learning"].artifact_id

print("\nPASS")