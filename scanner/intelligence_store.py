"""
AlphaRadar Intelligence Store

Persist and retrieve Intelligence Packages.

Responsibilities
----------------
- Save Intelligence Packages
- Load latest stored Intelligence Package

This module does NOT:
- serialize artifacts
- deserialize artifacts
- decide whether knowledge should be stored
- detect signals
- interpret markets
- make decisions
"""

from scanner.database import supabase

from scanner.knowledge_fingerprint import (
    build_knowledge_fingerprint,
)

from scanner.serializers.intelligence_serializer import (
    serialize_package,
)


# --------------------------------------------------
# Save
# --------------------------------------------------

def save_intelligence(package: dict):
    """
    Save an Intelligence Package.
    """

    serialized = serialize_package(
        package,
    )

    fingerprint = build_knowledge_fingerprint(
        package,
    )

    response = (

        supabase

        .table("intelligence_events")

        .insert(

            {

                "token":
                    serialized["token"],

                "decision":
                    serialized["decision"]["recommended_action"],

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

def load_latest_intelligence(
    token: str,
):
    """
    Load latest Intelligence Package.
    """

    response = (

        supabase

        .table("intelligence_events")

        .select("intelligence_package")

        .eq("token", token)

        .order(
            "created_at",
            desc=True,
        )

        .limit(1)

        .execute()

    )

    if not response.data:

        return None

    return response.data[0][
        "intelligence_package"
    ]