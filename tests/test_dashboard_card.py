"""
Dashboard Card Engineering Test
"""

from datetime import datetime, timezone
from pprint import pprint

from adaptive.dashboard.dashboard_card import (
    create_dashboard_card,
)


print()

print("=" * 60)
print("Dashboard Card Test")
print("=" * 60)

# --------------------------------------------------
# Build Dashboard Card
# --------------------------------------------------

card = create_dashboard_card(

    token="BTC",

    decision="WATCH",

    confidence="HIGH",

    historical_success=81.48,

    seen_before=True,

    reasons=[

        "ACCUMULATION",

        "STRONG_LIQUIDITY",

    ],

    summary="Bullish momentum detected.",

    last_updated=datetime.now(
        timezone.utc,
    ),

)

print()

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