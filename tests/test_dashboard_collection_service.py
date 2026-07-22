"""
Dashboard Collection Service Engineering Test
"""

from datetime import datetime, timezone
from pprint import pprint

from adaptive.compiler.experience_compiler import (
    compile_experience,
)

from adaptive.history.history_repository import (
    clear,
    save,
)

from application.dashboard_collection_service import (
    build_dashboard_collection,
)


print()

print("=" * 60)
print("Dashboard Collection Service Test")
print("=" * 60)

# --------------------------------------------------
# Clear Repository
# --------------------------------------------------

clear()

print()

print("Repository Cleared")
print("-" * 60)

# --------------------------------------------------
# Build Experiences
# --------------------------------------------------

experience_1 = compile_experience(

    fingerprint="WATCH|ACCUMULATION",

    success=True,

    timestamp=datetime.now(
        timezone.utc,
    ),

)

experience_2 = compile_experience(

    fingerprint="WATCH|ACCUMULATION",

    success=True,

    timestamp=datetime.now(
        timezone.utc,
    ),

)

experience_3 = compile_experience(

    fingerprint="WATCH|ACCUMULATION",

    success=False,

    timestamp=datetime.now(
        timezone.utc,
    ),

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

print()

print("Historical Experiences")
print("-" * 60)

pprint(
    experience_1,
)

pprint(
    experience_2,
)

pprint(
    experience_3,
)

# --------------------------------------------------
# Dashboard Inputs
# --------------------------------------------------

dashboards = [

    {

        "token":
            "BTC",

        "fingerprint":
            "WATCH|ACCUMULATION",

        "decision":
            "WATCH",

        "confidence":
            "HIGH",

        "summary":
            "Bullish momentum detected.",

        "reasons":[

            "ACCUMULATION",

            "STRONG_LIQUIDITY",

        ],

        "last_updated":
            datetime.now(
                timezone.utc,
            ),

    },

    {

        "token":
            "ETH",

        "fingerprint":
            "WATCH|ACCUMULATION",

        "decision":
            "WATCH",

        "confidence":
            "HIGH",

        "summary":
            "Bullish momentum detected.",

        "reasons":[

            "ACCUMULATION",

            "STRONG_LIQUIDITY",

        ],

        "last_updated":
            datetime.now(
                timezone.utc,
            ),

    },

]

# --------------------------------------------------
# Build Collection
# --------------------------------------------------

cards = build_dashboard_collection(

    dashboards=dashboards,

)

print()

print("Dashboard Cards")
print("-" * 60)

for card in cards:

    pprint(
        card,
    )

print()

# --------------------------------------------------
# Assertions
# --------------------------------------------------

assert len(cards) == 2

assert cards[0].token == "BTC"

assert cards[1].token == "ETH"

assert cards[0].decision == "WATCH"

assert cards[1].decision == "WATCH"

assert cards[0].confidence == "HIGH"

assert cards[1].confidence == "HIGH"

assert cards[0].historical_success == 66.67

assert cards[1].historical_success == 66.67

assert cards[0].seen_before is True

assert cards[1].seen_before is True

assert cards[0].metadata.engine_version == "1.0.0"

assert cards[1].metadata.engine_version == "1.0.0"

print("PASS")