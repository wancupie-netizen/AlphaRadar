"""
AlphaRadar Intelligence Store

Persist and retrieve Intelligence Packages.

Responsibilities
----------------
- Save Intelligence Packages
- Load latest stored Intelligence Package
- Serialize Intelligence Packages for storage

This module does NOT:
- decide whether knowledge should be stored
- detect signals
- interpret markets
- make decisions
"""

from scanner.database import supabase
from scanner.knowledge_fingerprint import build_knowledge_fingerprint


def _serialize_decision(decision: dict) -> dict:
    """
    Convert Decision payload into a JSON-safe structure.
    """

    return {
        "decision": (
            decision["decision"].value
            if hasattr(decision["decision"], "value")
            else decision["decision"]
        ),
        "confidence": decision["confidence"],
        "reasons": decision["reasons"],
    }


def _serialize_package(package: dict) -> dict:
    """
    Convert an Intelligence Package into a JSON-safe structure.
    """

    return {
        "token": package["token"],

        "observation": package["observation"],

        "signals": sorted(
            signal.value if hasattr(signal, "value") else signal
            for signal in package["signals"]
        ),

        "interpretations": sorted(
            interpretation.value
            if hasattr(interpretation, "value")
            else interpretation
            for interpretation in package["interpretations"]
        ),

        "decision": _serialize_decision(
            package["decision"]
        ),
    }


def save_intelligence(package: dict):
    """
    Save an Intelligence Package.
    """

    serialized_package = _serialize_package(package)

    fingerprint = build_knowledge_fingerprint(package)

    response = (
        supabase
        .table("intelligence_events")
        .insert({

            "token": serialized_package["token"],

            "decision": serialized_package["decision"]["decision"],

            "confidence": serialized_package["decision"]["confidence"],

            "knowledge_fingerprint": fingerprint,

            "intelligence_package": serialized_package,

        })
        .execute()
    )

    return response


def load_latest_intelligence(token: str):
    """
    Load the latest stored Intelligence Package.
    """

    response = (
        supabase
        .table("intelligence_events")
        .select("intelligence_package")
        .eq("token", token)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if not response.data:
        return None

    return response.data[0]["intelligence_package"]