"""
Tests for Founder Dashboard Shared Data.
"""

from datetime import (
    datetime,
    timezone,
)

import pytest

from adaptive.dashboard.dashboard_card import (
    create_dashboard_card,
)

from application.founder_dashboard_data import (
    serialize_founder_dashboard_results,
)


def build_test_card():
    """
    Build one reusable DashboardCard.
    """

    return create_dashboard_card(
        token="BTC",
        decision="WATCH",
        confidence="HIGH",
        historical_success=66.67,
        seen_before=True,
        reasons=[
            "STRONG_LIQUIDITY",
        ],
        summary="Momentum detected.",
        last_updated=datetime.now(
            timezone.utc,
        ),
    )


def test_should_serialize_available_coin():
    """
    Available cards should become JSON-safe data.
    """

    result = serialize_founder_dashboard_results(
        [
            {
                "token": "BTC",
                "card": build_test_card(),
                "error": None,
            }
        ]
    )[0]

    assert result["token"] == "BTC"

    assert result["available"] is True

    assert result["decision"] == "WATCH"

    assert result["confidence"] == "HIGH"

    assert result["historical_success"] == 66.67

    assert result["seen_before"] is True

    assert result["reasons"] == [
        "STRONG_LIQUIDITY",
    ]

    assert result["error"] is None


def test_should_serialize_unavailable_coin():
    """
    Failed scans should remain visible.
    """

    result = serialize_founder_dashboard_results(
        [
            {
                "token": "ETH",
                "card": None,
                "error": "Scan unavailable.",
            }
        ]
    )[0]

    assert result["token"] == "ETH"

    assert result["available"] is False

    assert result["decision"] is None

    assert result["error"] == (
        "Scan unavailable."
    )


def test_should_reject_invalid_collection():
    """
    Shared data requires a list.
    """

    with pytest.raises(
        ValueError,
        match=(
            "Founder dashboard results must be a list"
        ),
    ):
        serialize_founder_dashboard_results(
            None,
        )