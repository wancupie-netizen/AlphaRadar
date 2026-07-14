"""
Tests for Oscillation Pattern.
"""

from scanner.models import PatternResult
from scanner.patterns.oscillation import detect


def build_event(decision):

    return {
        "decision": decision,
        "confidence": "MEDIUM",
    }


def test_should_return_empty_when_history_is_empty():

    assert detect([]) == []


def test_should_return_empty_when_history_is_too_short():

    history = [

        build_event("WATCH"),

        build_event("REVIEW"),

    ]

    assert detect(history) == []


def test_should_detect_oscillation():

    history = [

        build_event("WATCH"),

        build_event("REVIEW"),

        build_event("WATCH"),

    ]

    patterns = detect(history)

    assert len(patterns) == 1

    pattern = patterns[0]

    assert isinstance(pattern, PatternResult)

    assert pattern.name == "Oscillation"

    assert pattern.confidence == 0.85


def test_should_not_detect_when_pattern_is_directional():

    history = [

        build_event("WATCH"),

        build_event("REVIEW"),

        build_event("IGNORE"),

    ]

    assert detect(history) == []


def test_should_not_detect_when_all_are_watch():

    history = [

        build_event("WATCH"),

        build_event("WATCH"),

        build_event("WATCH"),

    ]

    assert detect(history) == []