"""
AlphaRadar Knowledge Gate

Decide whether an Intelligence Package deserves
to become persistent knowledge.

Responsibilities
----------------
- Compare current and previous Intelligence Packages
- Detect meaningful intelligence changes
- Decide whether to store knowledge

This module does NOT:
- access databases
- save data
- publish feeds
- generate fingerprints
"""


def _normalize_interpretations(package: dict) -> set[str]:
    """
    Normalize interpretations into a comparable set.
    """

    return {
        item.value if hasattr(item, "value") else str(item)
        for item in package.get("interpretations", [])
    }


def should_store(
    current: dict,
    previous: dict | None,
) -> bool:
    """
    Decide whether the current Intelligence Package
    should be stored.
    """

    # ---------------------------------------
    # First knowledge
    # ---------------------------------------

    if previous is None:
        return True

    # ---------------------------------------
    # Decision changed
    # ---------------------------------------

    current_decision = (
        current
        .get("decision", {})
        .get("decision")
    )

    previous_decision = (
        previous
        .get("decision", {})
        .get("decision")
    )

    if current_decision != previous_decision:
        return True

    # ---------------------------------------
    # Interpretation changed
    # ---------------------------------------

    if (
        _normalize_interpretations(current)
        !=
        _normalize_interpretations(previous)
    ):
        return True

    # ---------------------------------------
    # No meaningful change
    # ---------------------------------------

    return False