"""
Dashboard Request Builder Engineering Test
"""

from datetime import datetime, timezone
from pprint import pprint

from adaptive.dashboard.dashboard_request import (
    DashboardRequest,
)

from adaptive.dashboard.dashboard_request_builder import (
    build_dashboard_request,
)

from core.artifacts.decision_artifact import (
    DecisionArtifact,
    DecisionContext,
    DecisionMetadata,
    Reason,
)


print()

print("=" * 60)
print("Dashboard Request Builder Test")
print("=" * 60)

# --------------------------------------------------
# Decision Artifact
# --------------------------------------------------

decision = DecisionArtifact(

    recommended_action="WATCH",

    confidence="HIGH",

    summary="Bullish momentum detected.",

    context=DecisionContext(),

    reasons=(

        Reason(

            title="ACCUMULATION",

        ),

        Reason(

            title="STRONG_LIQUIDITY",

        ),

    ),

    metadata=DecisionMetadata(

        engine_version="1.0.0",

        symbol="BTC",

        pair="BTC",

    ),

)

print()

print("Decision Artifact")
print("-" * 60)

pprint(
    decision,
)

# --------------------------------------------------
# Dashboard Request
# --------------------------------------------------

request = build_dashboard_request(

    token="BTC",

    decision=decision,

    knowledge_fingerprint=(
        "7d87405ce3b3c54af804cc25cb31e3b3"
        "e091d33f77783df3cb4a06c888abaa99"
    ),

    last_updated=datetime.now(
        timezone.utc,
    ),

)

print()

print("Dashboard Request")
print("-" * 60)

pprint(
    request,
)

print()

# --------------------------------------------------
# Assertions
# --------------------------------------------------

assert isinstance(
    request,
    DashboardRequest,
)

assert request.token == "BTC"

assert (
    request.decision
    is decision
)

assert (
    request.decision.recommended_action
    == "WATCH"
)

assert (
    request.decision.confidence
    == "HIGH"
)

assert (
    request.decision.summary
    == "Bullish momentum detected."
)

assert (
    request.knowledge_fingerprint
    ==
    "7d87405ce3b3c54af804cc25cb31e3b3"
    "e091d33f77783df3cb4a06c888abaa99"
)

assert (
    request.metadata.engine_version
    == "1.0.0"
)

assert request.request_id.startswith(
    "DBR-"
)

print("PASS")