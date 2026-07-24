"""
Adaptive Dashboard Service Engineering Test
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

from application.adaptive_dashboard_service import (
    build_adaptive_dashboard,
)

from scanner.knowledge_fingerprint import (
    build_knowledge_fingerprint,
)

from scanner.decision_types import (
    DecisionType,
)

from scanner.signal_types import (
    SignalType,
)

from scanner.interpretation_types import (
    InterpretationType,
)


print()

print("=" * 60)
print("Adaptive Dashboard Service Test")
print("=" * 60)

# --------------------------------------------------
# Clear Repository
# --------------------------------------------------

clear()

print()

print("Repository Cleared")
print("-" * 60)

# --------------------------------------------------
# Intelligence Package
# --------------------------------------------------

intelligence_package = {

    "observation": {

        "observation_types": [

            "PRICE_BREAKOUT",

            "HIGH_VOLUME",

        ],

    },

    "signals": [

        SignalType.PRICE_UP,

        SignalType.VOLUME_UP,

        SignalType.LIQUIDITY_UP,

    ],

    "interpretations": [

        InterpretationType.ACCUMULATION,

        InterpretationType.STRONG_LIQUIDITY,

    ],

    "decision": DecisionType.WATCH,

    "confidence": "HIGH",

    "summary": "Bullish momentum detected.",

}

print()

print("Intelligence Package")
print("-" * 60)

pprint(
    intelligence_package,
)

# --------------------------------------------------
# Build Knowledge Fingerprint
# --------------------------------------------------

fingerprint = build_knowledge_fingerprint(

    intelligence_package,

)

print()

print("Knowledge Fingerprint")
print("-" * 60)

print(
    fingerprint,
)

# --------------------------------------------------
# Build Experiences
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
# Build Dashboard
# --------------------------------------------------

dashboard = build_adaptive_dashboard(

    token="BTC",

    intelligence_package=intelligence_package,

    last_updated=datetime.now(
        timezone.utc,
    ),

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

assert dashboard.seen_before is True

assert dashboard.historical_success == 66.67

assert dashboard.summary == "Bullish momentum detected."

assert dashboard.reasons == [

    "ACCUMULATION",

    "STRONG_LIQUIDITY",

]

assert dashboard.metadata.engine_version == "1.0.0"

print("PASS")