"""
Fingerprint Builder Engineering Test
"""

from pprint import pprint

from adaptive.identity.fingerprint_builder import (
    build_fingerprint,
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
print("Fingerprint Builder Test")
print("=" * 60)

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

}

print()

print("Intelligence Package")
print("-" * 60)

pprint(
    intelligence_package,
)

# --------------------------------------------------
# Build Fingerprint
# --------------------------------------------------

fingerprint = build_fingerprint(

    intelligence_package,

)

print()

print("Fingerprint")
print("-" * 60)

print(
    fingerprint,
)

print()

# --------------------------------------------------
# Assertions
# --------------------------------------------------

assert isinstance(
    fingerprint,
    str,
)

assert len(
    fingerprint,
) == 64

assert fingerprint == build_fingerprint(
    intelligence_package,
)

print("PASS")