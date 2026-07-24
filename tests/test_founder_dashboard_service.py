"""
Tests for AlphaRadar Founder Dashboard Service.
"""

from datetime import datetime, timezone

from adaptive.dashboard.dashboard_card import (
    create_dashboard_card,
)

from application.founder_dashboard_service import (
    FOUNDER_TOKENS,
    build_founder_dashboard_results,
)


def build_test_card(
    token: str,
):
    """
    Build a reusable DashboardCard.
    """

    return create_dashboard_card(

        token=token,

        decision="WATCH",

        confidence="HIGH",

        historical_success=66.67,

        seen_before=True,

        reasons=[
            "MOMENTUM",
        ],

        summary="Market intelligence available.",

        last_updated=datetime.now(
            timezone.utc,
        ),

    )


def test_should_define_five_founder_tokens():
    """
    Founder MVP must expose the approved five coins.
    """

    assert FOUNDER_TOKENS == (
        "BTC",
        "ETH",
        "SOL",
        "XRP",
        "SUI",
    )


def test_should_scan_tokens_sequentially():
    """
    Service should preserve token ordering.
    """

    scanned_tokens: list[str] = []

    def fake_scan(
        token: str,
    ) -> dict:

        scanned_tokens.append(
            token,
        )

        return {
            "success": True,
            "dashboard": build_test_card(
                token,
            ),
        }

    results = build_founder_dashboard_results(
        scan=fake_scan,
    )

    assert scanned_tokens == list(
        FOUNDER_TOKENS,
    )

    assert [
        result["token"]
        for result in results
    ] == list(
        FOUNDER_TOKENS,
    )

    assert len(
        results,
    ) == 5


def test_should_preserve_successful_dashboard_card():
    """
    Successful scans should expose DashboardCard.
    """

    def fake_scan(
        token: str,
    ) -> dict:

        return {
            "success": True,
            "dashboard": build_test_card(
                token,
            ),
        }

    results = build_founder_dashboard_results(

        tokens=[
            "btc",
        ],

        scan=fake_scan,

    )

    result = results[0]

    assert result["token"] == "BTC"

    assert result["card"].token == "BTC"

    assert result["error"] is None


def test_should_preserve_failed_coin_and_continue():
    """
    One failed coin must not hide remaining coins.
    """

    def fake_scan(
        token: str,
    ) -> dict:

        if token == "ETH":

            return {
                "success": False,
                "error": "ETH scan unavailable.",
            }

        return {
            "success": True,
            "dashboard": build_test_card(
                token,
            ),
        }

    results = build_founder_dashboard_results(

        tokens=[
            "BTC",
            "ETH",
            "SOL",
        ],

        scan=fake_scan,

    )

    assert len(
        results,
    ) == 3

    assert results[0]["card"] is not None

    assert results[1]["card"] is None

    assert results[1]["error"] == (
        "ETH scan unavailable."
    )

    assert results[2]["card"] is not None