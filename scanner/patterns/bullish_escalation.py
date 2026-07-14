"""
Bullish Escalation Pattern

Pattern
-------
IGNORE
REVIEW
WATCH

Meaning
-------
Decision quality has improved across
three consecutive Intelligence Events.
"""

from scanner.models import PatternResult


def detect(history):
    """
    Detect Bullish Escalation.
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

        "IGNORE",

    ]:

        return []

    return [

        PatternResult(

            name="Bullish Escalation",

            confidence=0.95,

            description=(
                "Decision quality has improved across "
                "three consecutive knowledge events."
            ),

        )

    ]