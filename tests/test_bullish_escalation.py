"""
Tests for Bullish Escalation Pattern.
"""

from scanner.patterns.bullish_escalation import detect
from scanner.models import PatternResult


def build_event(decision):

    return {
        "decision": decision,
        "confidence": "MEDIUM",
    }


# ==================================================
# Empty History
# ==================================================

def test_should_return_empty_when_history_is_empty():

    patterns = detect([])

    assert patterns == []


# ==================================================
# Not Enough History
# ==================================================

def test_should_return_empty_when_history_is_too_short():

    history = [

        build_event("WATCH"),

        build_event("REVIEW"),

    ]

    patterns = detect(history)

    assert patterns == []


# ==================================================
# Bullish Escalation
# ==================================================

def test_should_detect_bullish_escalation():

    history = [

        build_event("WATCH"),

        build_event("REVIEW"),

        build_event("IGNORE"),

    ]

    patterns = detect(history)

    assert len(patterns) == 1

    pattern = patterns[0]

    assert isinstance(
        pattern,
        PatternResult,
    )

    assert pattern.name == "Bullish Escalation"

    assert pattern.confidence == 0.95

    assert (
        "Decision quality has improved"
        in pattern.description
    )


# ==================================================
# Wrong Order
# ==================================================

def test_should_not_detect_when_order_is_incorrect():

    history = [

        build_event("REVIEW"),

        build_event("WATCH"),

        build_event("IGNORE"),

    ]

    patterns = detect(history)

    assert patterns == []


# ==================================================
# Same Decisions
# ==================================================

def test_should_not_detect_when_all_decisions_are_the_same():

    history = [

        build_event("WATCH"),

        build_event("WATCH"),

        build_event("WATCH"),

    ]

    patterns = detect(history)

    assert patterns == []