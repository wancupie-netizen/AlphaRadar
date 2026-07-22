"""
Dashboard Context Engineering Test
"""

from datetime import datetime, timezone
from pprint import pprint

from adaptive.artifacts.evidence_artifact import (
    create_evidence,
)

from adaptive.dashboard.dashboard_context import (
    create_dashboard_context,
)


print()

print("=" * 60)
print("Dashboard Context Test")
print("=" * 60)

# --------------------------------------------------
# Build Evidence
# --------------------------------------------------

evidence = create_evidence(

    seen_before=True,

    sample_size=27,

    success_rate=81.48,

    last_seen=datetime.now(
        timezone.utc,
    ),

)

# --------------------------------------------------
# Build Dashboard Context
# --------------------------------------------------

context = create_dashboard_context(

    token="BTC",

    decision="WATCH",

    confidence="HIGH",

    summary="Bullish momentum detected.",

    reasons=[

        "ACCUMULATION",

        "STRONG_LIQUIDITY",

    ],

    evidence=evidence,

    updated_at=datetime.now(
        timezone.utc,
    ),

)

print()

pprint(context)

print()

# --------------------------------------------------
# Assertions
# --------------------------------------------------

assert context.token == "BTC"

assert context.decision == "WATCH"

assert context.confidence == "HIGH"

assert context.summary == "Bullish momentum detected."

assert len(context.reasons) == 2

assert context.reasons[0] == "ACCUMULATION"

assert context.reasons[1] == "STRONG_LIQUIDITY"

assert context.evidence.seen_before is True

assert context.evidence.sample_size == 27

assert context.evidence.success_rate == 81.48

assert context.evidence.metadata.engine_version == "1.0.0"

print("PASS")