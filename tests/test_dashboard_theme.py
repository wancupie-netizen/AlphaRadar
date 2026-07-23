"""
Tests for Dashboard Theme.
"""

from presentation.dashboard_theme import (
    THEME,
    build_dashboard_css,
    decision_colour,
)


def test_should_return_watch_colour():

    assert decision_colour(
        "WATCH",
    ) == THEME["watch"]


def test_should_return_buy_colour():

    assert decision_colour(
        "BUY",
    ) == THEME["buy"]


def test_should_return_sell_colour():

    assert decision_colour(
        "SELL",
    ) == THEME["sell"]


def test_should_return_unknown_colour():

    assert decision_colour(
        "HELLO",
    ) == THEME["unknown"]


def test_should_build_dashboard_css():

    css = build_dashboard_css()

    assert "background" in css

    assert ".card" in css

    assert ".badge" in css