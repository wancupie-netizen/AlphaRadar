"""
Persistent Watch Pattern

Pattern
-------
WATCH
WATCH
WATCH

Meaning
-------
The token has remained in WATCH state across
three consecutive Intelligence Events.
"""

from scanner.models import PatternResult


def detect(history):
    """
    Detect Persistent Watch.

    Parameters
    ----------
    history : list[dict]

    Returns
    -------
    list[PatternResult]
    """

    if len(history) < 3:
        return []

    decisions = [

        item["decision"]

        for item in history[:3]

    ]

    if decisions != [

        "WATCH",

        "WATCH",

        "WATCH",

    ]:

        return []

    return [

        PatternResult(

            name="Persistent Watch",

            confidence=0.90,

            description=(
                "WATCH has appeared in the last "
                "three consecutive knowledge events."
            ),

        )

    ]