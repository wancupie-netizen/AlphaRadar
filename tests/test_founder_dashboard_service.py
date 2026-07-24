"""
Tests for AlphaRadar Founder Dashboard Service.
"""

from datetime import (
    datetime,
    timezone,
)

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
        summary=(
            "Market intelligence available."
        ),
        last_updated=datetime.now(
            timezone.utc,
        ),
    )


def test_should_keep_founder_fallback_tokens():
    """
    Existing five-token reference remains available.
    """

    assert FOUNDER_TOKENS == (
        "BTC",
        "ETH",
        "SOL",
        "XRP",
        "SUI",
    )


def test_should_load_ranked_universe_by_default():
    """
    Default service should use the universe loader.
    """

    scanned_tokens: list[str] = []

    def fake_universe_loader():

        return (
            "BTC",
            "ETH",
            "SOL",
        )

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
        universe_loader=fake_universe_loader,
    )

    assert scanned_tokens == [
        "BTC",
        "ETH",
        "SOL",
    ]

    assert [
        result["token"]
        for result in results
    ] == [
        "BTC",
        "ETH",
        "SOL",
    ]


def test_should_accept_explicit_token_collection():
    """
    Explicit tokens should bypass universe loading.
    """

    def failing_universe_loader():

        raise AssertionError(
            "Universe loader should not be called."
        )

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
        universe_loader=failing_universe_loader,
    )

    assert results[0]["token"] == "BTC"

    assert results[0]["card"].token == "BTC"

    assert results[0]["error"] is None


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
                "error": (
                    "ETH scan unavailable."
                ),
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


def test_should_preserve_unsupported_symbol_and_continue():
    """
    Unsupported CoinMarketCap symbols must not stop scanning.
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
        tokens=[
            "BTC",
            "币安人生",
            "ETH",
        ],
        scan=fake_scan,
    )

    assert scanned_tokens == [
        "BTC",
        "ETH",
    ]

    assert len(
        results,
    ) == 3

    assert results[1]["token"] == (
        "币安人生"
    )

    assert results[1]["card"] is None

    assert (
        "unsupported characters"
        in results[1]["error"]
    )

    assert results[2]["card"] is not None