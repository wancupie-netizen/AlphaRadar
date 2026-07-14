"""
Oscillation Pattern

Pattern
-------
WATCH
REVIEW
WATCH

Meaning
-------
Decision oscillates without maintaining
a consistent direction.
"""

from scanner.models import PatternResult


def detect(history):
    """
    Detect Oscillation.
    """

    if len(history) < 3:
        return []

    decisions = [

        event["decision"]

        for event in history[:3]

    ]

    if decisions != [

        "WATCH",

        "REVIEW",

        "WATCH",

    ]:

        return []

    return [

        PatternResult(

            name="Oscillation",

            confidence=0.85,

            description=(
                "Decision is oscillating without "
                "forming a stable trend."
            ),

        )

    ]