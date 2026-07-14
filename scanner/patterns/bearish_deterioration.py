"""
Bearish Deterioration Pattern

Pattern
-------
WATCH
REVIEW
IGNORE

Meaning
-------
Decision quality has weakened across
three consecutive Intelligence Events.
"""

from scanner.models import PatternResult


def detect(history):
    """
    Detect Bearish Deterioration.
    """

    if len(history) < 3:
        return []

    decisions = [

        event["decision"]

        for event in history[:3]

    ]

    if decisions != [

        "IGNORE",

        "REVIEW",

        "WATCH",

    ]:

        return []

    return [

        PatternResult(

            name="Bearish Deterioration",

            confidence=0.95,

            description=(
                "Decision quality has weakened across "
                "three consecutive knowledge events."
            ),

        )

    ]