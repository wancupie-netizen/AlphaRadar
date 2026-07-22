"""
Adaptive Dashboard Service Engineering Test
"""

from datetime import datetime, timezone
from pprint import pprint

from adaptive.compiler.experience_compiler import (
    compile_experience,
)

from adaptive.dashboard.dashboard_request_builder import (
    build_dashboard_request,
)

from adaptive.history.history_repository import (
    clear,
    save,
)

from application.adaptive_dashboard_service import (
    build_adaptive_dashboard,
)

from core.artifacts.decision_artifact import (
    DecisionArtifact,
    DecisionContext,
    DecisionMetadata,
    Reason,
)


print()

print("=" * 60)
print("Adaptive Dashboard Service Test")
print("=" * 60)

# --------------------------------------------------
# Repository
# --------------------------------------------------

clear()

print()

print("Repository Cleared")
print("-" * 60)

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
# Knowledge Fingerprint
# --------------------------------------------------

fingerprint = (
    "7d87405ce3b3c54af804cc25cb31e3b3"
    "e091d33f77783df3cb4a06c888abaa99"
)

# --------------------------------------------------
# Historical Experiences
# --------------------------------------------------

experience_1 = compile_experience(

    fingerprint=fingerprint,

    success=True,

    timestamp=datetime.now(
        timezone.utc,
    ),

)

experience_2 = compile_experience(

    fingerprint=fingerprint,

    success=True,

    timestamp=datetime.now(
        timezone.utc,
    ),

)

experience_3 = compile_experience(

    fingerprint=fingerprint,

    success=False,

    timestamp=datetime.now(
        timezone.utc,
    ),

)

print()

print("Experience #1")
print("-" * 60)

pprint(
    experience_1,
)

print()

print("Experience #2")
print("-" * 60)

pprint(
    experience_2,
)

print()

print("Experience #3")
print("-" * 60)

pprint(
    experience_3,
)

save(
    experience_1,
)

save(
    experience_2,
)

save(
    experience_3,
)

# --------------------------------------------------
# Dashboard Request
# --------------------------------------------------

request = build_dashboard_request(

    token="BTC",

    decision=decision,

    knowledge_fingerprint=fingerprint,

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

# --------------------------------------------------
# Dashboard Card
# --------------------------------------------------

dashboard = build_adaptive_dashboard(

    request,

)

print()

print("Dashboard Card")
print("-" * 60)

pprint(
    dashboard,
)

print()

# --------------------------------------------------
# Assertions
# --------------------------------------------------

assert dashboard.token == "BTC"

assert dashboard.decision == "WATCH"

assert dashboard.confidence == "HIGH"

assert dashboard.summary == "Bullish momentum detected."

assert dashboard.reasons == [

    "ACCUMULATION",

    "STRONG_LIQUIDITY",

]

assert dashboard.seen_before is True

assert dashboard.historical_success == 66.67

assert dashboard.metadata.engine_version == "1.0.0"

print("PASS")