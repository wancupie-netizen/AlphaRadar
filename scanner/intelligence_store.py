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

from core.artifacts.decision_artifact import DecisionArtifact

from scanner.database import supabase
from scanner.knowledge_fingerprint import (
    build_knowledge_fingerprint,
)


# --------------------------------------------------
# Decision Serialization
# --------------------------------------------------

def _serialize_decision(decision) -> dict:
    """
    Convert Decision into a JSON-safe structure.

    Supports:
    - DecisionArtifact
    - Legacy dict
    """

    if isinstance(decision, DecisionArtifact):

        return {

            "artifact_id":
                decision.artifact_id,

            "decision":
                decision.recommended_action,

            "confidence":
                decision.confidence,

            "summary":
                decision.summary,

            "reasons": [

                {

                    "title":
                        reason.title,

                    "description":
                        reason.description,

                    "evidence": [

                        {

                            "name":
                                evidence.name,

                            "value":
                                evidence.value,

                            "source":
                                evidence.source,

                        }

                        for evidence in reason.evidence

                    ],

                }

                for reason in decision.reasons

            ],

        }

    # --------------------------------------------
    # Legacy compatibility
    # --------------------------------------------

    return {

        "decision":
            decision.get("decision"),

        "confidence":
            decision.get("confidence"),

        "reasons":
            decision.get("reasons", []),

    }


# --------------------------------------------------
# Package Serialization
# --------------------------------------------------

def _serialize_package(package: dict) -> dict:
    """
    Convert Intelligence Package into JSON-safe structure.
    """

    return {

        "token":
            package["token"],

        "observation":
            package["observation"],

        "signals":

            sorted(

                signal.value
                if hasattr(signal, "value")
                else signal

                for signal in package["signals"]

            ),

        "interpretations":

            sorted(

                interpretation.value
                if hasattr(
                    interpretation,
                    "value",
                )
                else interpretation

                for interpretation
                in package["interpretations"]

            ),

        "decision":

            _serialize_decision(
                package["decision"]
            ),

    }


# --------------------------------------------------
# Save
# --------------------------------------------------

def save_intelligence(package: dict):

    serialized = _serialize_package(package)

    fingerprint = build_knowledge_fingerprint(
        package
    )

    response = (

        supabase

        .table("intelligence_events")

        .insert(

            {

                "token":
                    serialized["token"],

                "decision":
                    serialized["decision"]["decision"],

                "confidence":
                    serialized["decision"]["confidence"],

                "knowledge_fingerprint":
                    fingerprint,

                "intelligence_package":
                    serialized,

            }

        )

        .execute()

    )

    return response


# --------------------------------------------------
# Load
# --------------------------------------------------

def load_latest_intelligence(token: str):

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