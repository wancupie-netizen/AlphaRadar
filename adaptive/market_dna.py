from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Any, Dict


@dataclass(frozen=True)
class MarketDNA:
    """
    Canonical representation of a market state.

    dna:
        Human-readable identity string.

    hash:
        Stable SHA-256 fingerprint of the DNA.

    features:
        Canonical features used to build the DNA.
    """

    dna: str
    hash: str
    features: Dict[str, Any]


# ---------------------------------------------------------------------
# Canonical mappings
# ---------------------------------------------------------------------

TREND_MAP = {
    "UPTREND": "UPTREND",
    "DOWNTREND": "DOWNTREND",
    "SIDEWAYS": "SIDEWAYS",
}

VOLATILITY_MAP = {
    "LOW": "LOWVOL",
    "MEDIUM": "MIDVOL",
    "HIGH": "HIGHVOL",
}

VOLUME_MAP = {
    "LOW": "LOWVOLM",
    "MEDIUM": "MIDVOLM",
    "HIGH": "HIGHVOLM",
}

LIQUIDITY_MAP = {
    "LOW": "LOWLIQ",
    "GOOD": "GOODLIQ",
    "HIGH": "HIGHLIQ",
}

STRUCTURE_MAP = {
    "BREAKOUT": "BREAKOUT",
    "BREAKDOWN": "BREAKDOWN",
    "RANGE": "RANGE",
    "REVERSAL": "REVERSAL",
}

MOMENTUM_MAP = {
    "WEAK": "WEAK",
    "NORMAL": "NORMAL",
    "STRONG": "STRONG",
}


def _canonical(value: Any, mapping: Dict[str, str], default: str) -> str:
    if value is None:
        return default
    return mapping.get(str(value).upper(), default)


def build_market_dna(context: Dict[str, Any]) -> MarketDNA:
    """
    Build a canonical Market DNA from a DecisionContext.

    This function is deterministic:
    identical input -> identical DNA -> identical hash.
    """

    features = {
        "trend": _canonical(
            context.get("trend"),
            TREND_MAP,
            "UNKNOWN",
        ),
        "volatility": _canonical(
            context.get("volatility"),
            VOLATILITY_MAP,
            "UNKNOWNVOL",
        ),
        "volume": _canonical(
            context.get("volume"),
            VOLUME_MAP,
            "UNKNOWNVOLM",
        ),
        "liquidity": _canonical(
            context.get("liquidity"),
            LIQUIDITY_MAP,
            "UNKNOWNLIQ",
        ),
        "market_structure": _canonical(
            context.get("market_structure"),
            STRUCTURE_MAP,
            "UNKNOWNSTRUCT",
        ),
        "momentum": _canonical(
            context.get("momentum"),
            MOMENTUM_MAP,
            "UNKNOWNMOM",
        ),
    }

    dna = "-".join(features.values())

    fingerprint = sha256(
        dna.encode("utf-8")
    ).hexdigest().upper()

    return MarketDNA(
        dna=dna,
        hash=fingerprint,
        features=features,
    )