"""
Dashboard Service Engineering Test
"""

from datetime import datetime, timezone
from pprint import pprint

from adaptive.compiler.experience_compiler import (
    compile_experience,
)

from application.dashboard_service import (
    build_dashboard,
)


print()

print("=" * 60)
print("Dashboard Service Test")
print("=" * 60)

# --------------------------------------------------
# Build Experience
# --------------------------------------------------

experience = compile_experience(

    fingerprint="WATCH|ACCUMULATION",

    success=True,

    timestamp=datetime.now(
        timezone.utc,
    ),

)

print()

print("Experience")
print("-" * 60)

pprint(experience)

# --------------------------------------------------
# Build Dashboard
# --------------------------------------------------

dashboard = build_dashboard(

    token="BTC",

    decision="WATCH",

    confidence="HIGH",

    summary="Bullish momentum detected.",

    reasons=[

        "ACCUMULATION",

        "STRONG_LIQUIDITY",

    ],

    experience=experience,

    updated_at=datetime.now(
        timezone.utc,
    ),

)

print()

print("Dashboard")
print("-" * 60)

pprint(dashboard)

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

# --------------------------------------------------
# Evidence Assertions
# --------------------------------------------------

assert dashboard.evidence.seen_before is True

assert dashboard.evidence.sample_size == 1

assert dashboard.evidence.success_rate == 100.0

assert dashboard.evidence.last_seen == experience.last_seen

assert dashboard.evidence.metadata.engine_version == "1.0.0"

assert dashboard.updated_at is not None

print("PASS")