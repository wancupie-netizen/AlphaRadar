"""
Tests for Bearish Deterioration Pattern.
"""

from scanner.models import PatternResult
from scanner.patterns.bearish_deterioration import detect


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

        build_event("IGNORE"),

        build_event("REVIEW"),

    ]

    patterns = detect(history)

    assert patterns == []


# ==================================================
# Bearish Deterioration
# ==================================================

def test_should_detect_bearish_deterioration():

    history = [

        build_event("IGNORE"),

        build_event("REVIEW"),

        build_event("WATCH"),

    ]

    patterns = detect(history)

    assert len(patterns) == 1

    pattern = patterns[0]

    assert isinstance(
        pattern,
        PatternResult,
    )

    assert pattern.name == "Bearish Deterioration"

    assert pattern.confidence == 0.95

    assert (
        "Decision quality has weakened"
        in pattern.description
    )


# ==================================================
# Wrong Order
# ==================================================

def test_should_not_detect_when_order_is_incorrect():

    history = [

        build_event("WATCH"),

        build_event("REVIEW"),

        build_event("IGNORE"),

    ]

    patterns = detect(history)

    assert patterns == []


# ==================================================
# Same Decisions
# ==================================================

def test_should_not_detect_when_all_decisions_are_the_same():

    history = [

        build_event("IGNORE"),

        build_event("IGNORE"),

        build_event("IGNORE"),

    ]

    patterns = detect(history)

    assert patterns == []