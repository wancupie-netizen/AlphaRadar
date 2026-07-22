"""
Dashboard Builder Engineering Test
"""

from datetime import datetime, timezone
from pprint import pprint

from adaptive.dashboard.dashboard_builder import (
    build_dashboard_card,
)

from adaptive.history.history_summary import (
    create_history_summary,
)


print()

print("=" * 60)
print("Dashboard Builder Test")
print("=" * 60)

# --------------------------------------------------
# Build History Summary
# --------------------------------------------------

history = create_history_summary(

    seen_before=True,

    sample_size=27,

    most_common_outcome="SUCCESS",

    outcome_occurrence=22,

    success_rate=81.48,

    average_duration_hours=18.0,

    last_seen=datetime.now(
        timezone.utc,
    ),

)

print()

print("History Summary")
print("-" * 60)

pprint(
    history,
)

# --------------------------------------------------
# Build Dashboard Card
# --------------------------------------------------

card = build_dashboard_card(

    token="BTC",

    decision="WATCH",

    confidence="HIGH",

    summary="Bullish momentum detected.",

    reasons=[

        "ACCUMULATION",

        "STRONG_LIQUIDITY",

    ],

    history=history,

    last_updated=datetime.now(
        timezone.utc,
    ),

)

print()

print("Dashboard Card")
print("-" * 60)

pprint(
    card,
)

print()

# --------------------------------------------------
# Assertions
# --------------------------------------------------

assert card.token == "BTC"

assert card.decision == "WATCH"

assert card.confidence == "HIGH"

assert card.historical_success == 81.48

assert card.seen_before is True

assert card.reasons == [

    "ACCUMULATION",

    "STRONG_LIQUIDITY",

]

assert card.summary == "Bullish momentum detected."

assert card.metadata.engine_version == "1.0.0"

print("PASS")