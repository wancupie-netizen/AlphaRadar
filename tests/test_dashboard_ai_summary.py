"""
Tests for AI Summary component.
"""

import pytest

from presentation.dashboard_components.ai_summary import (
    normalize_summary,
    render_ai_summary_panel,
)


def test_should_render_summary():

    html = render_ai_summary_panel(

        summary="Bullish breakout detected.",

    )

    assert "Intelligence Summary" in html

    assert "Bullish breakout detected." in html

    assert "summary-panel" in html


def test_should_render_empty_summary():

    html = render_ai_summary_panel(

        summary="   ",

    )

    assert (
        "No intelligence summary is currently available."
        in html
    )


def test_should_escape_html():

    html = render_ai_summary_panel(

        summary="<script>alert(1)</script>",

    )

    assert "<script>" not in html

    assert "&lt;script&gt;" in html


def test_should_normalize_summary():

    assert normalize_summary(

        " Momentum "

    ) == "Momentum"


def test_should_reject_non_string():

    with pytest.raises(

        ValueError,

        match="Dashboard summary must be a string",

    ):

        normalize_summary(
            None,
        )