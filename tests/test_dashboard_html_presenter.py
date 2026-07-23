"""
Tests for AlphaRadar Dashboard HTML Presenter.
"""

from datetime import datetime, timezone

from adaptive.dashboard.dashboard_card import (
    create_dashboard_card,
)

from presentation.dashboard_html_presenter import (
    render_dashboard_html,
)


# ==========================================================
# Complete Dashboard
# ==========================================================

def test_should_render_dashboard_card_as_html():
    """
    Presenter should render all official DashboardCard fields.
    """

    card = create_dashboard_card(

        token="BTC",

        decision="WATCH",

        confidence="HIGH",

        historical_success=66.67,

        seen_before=True,

        reasons=[
            "ACCUMULATION",
            "STRONG_LIQUIDITY",
        ],

        summary="Bullish momentum detected.",

        last_updated=datetime(
            2026,
            7,
            22,
            10,
            30,
            tzinfo=timezone.utc,
        ),

    )

    html = render_dashboard_html(
        card,
    )

    assert "<!DOCTYPE html>" in html

    assert "ALPHARADAR" in html

    assert "BTC" in html

    assert "WATCH" in html

    assert "HIGH Confidence" in html

    assert "66.67%" in html

    assert "Seen Before" in html

    assert "Bullish momentum detected." in html

    assert "ACCUMULATION" in html

    assert "STRONG_LIQUIDITY" in html

    assert "2026-07-22 10:30:00+00:00" in html

    assert "Engine 1.0.0" in html


# ==========================================================
# Safe HTML
# ==========================================================

def test_should_escape_dynamic_html_values():
    """
    Presenter must escape all user or data-derived text.
    """

    card = create_dashboard_card(

        token="<script>alert('token')</script>",

        decision="<b>WATCH</b>",

        confidence="HIGH",

        historical_success=0.0,

        seen_before=False,

        reasons=[
            "<img src=x onerror=alert(1)>",
        ],

        summary="<script>alert('summary')</script>",

        last_updated=datetime.now(
            timezone.utc,
        ),

    )

    html = render_dashboard_html(
        card,
    )

    assert "<script>alert('token')</script>" not in html

    assert "&lt;script&gt;" in html

    assert "<img src=x onerror=alert(1)>" not in html

    assert "&lt;img src=x onerror=alert(1)&gt;" in html


# ==========================================================
# Empty Reasons
# ==========================================================

def test_should_render_empty_reason_state():
    """
    Presenter should display a clear state when reasons are empty.
    """

    card = create_dashboard_card(

        token="ETH",

        decision="WATCH",

        confidence="MEDIUM",

        historical_success=0.0,

        seen_before=False,

        reasons=[],

        summary="No historical evidence available.",

        last_updated=datetime.now(
            timezone.utc,
        ),

    )

    html = render_dashboard_html(
        card,
    )

    assert "No decision reasons available." in html

    assert "New Pattern" in html

    assert "MEDIUM Confidence" in html