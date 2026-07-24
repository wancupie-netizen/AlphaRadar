"""
Tests for AlphaRadar Telegram Notifier.
"""

import pytest

from application.telegram_notifier import (
    build_telegram_message,
    send_telegram_alert,
)


DASHBOARD_DATA = [
    {
        "token": "BTC",
        "available": True,
        "decision": "WATCH",
        "confidence": "HIGH",
        "historical_success": 66.67,
        "seen_before": True,
        "reasons": [
            "STRONG_LIQUIDITY",
            "PRICE_MOMENTUM",
        ],
        "summary": "Momentum detected.",
        "error": None,
    },
    {
        "token": "ETH",
        "available": False,
        "decision": None,
        "confidence": None,
        "historical_success": None,
        "seen_before": False,
        "reasons": [],
        "summary": None,
        "error": "Dashboard unavailable.",
    },
]


class FakeResponse:
    """
    Minimal successful requests response.
    """

    def raise_for_status(
        self,
    ) -> None:
        return None


def test_should_build_telegram_message():
    """
    Message should expose shared engine data.
    """

    message = build_telegram_message(
        DASHBOARD_DATA,
    )

    assert "AlphaRadar Founder Alert" in message

    assert "BTC" in message

    assert "WATCH" in message

    assert "HIGH" in message

    assert "66.67%" in message

    assert "STRONG_LIQUIDITY" in message

    assert "ETH" in message

    assert "UNAVAILABLE" in message


def test_should_send_telegram_alert():
    """
    Notifier should call Telegram sendMessage once.
    """

    calls: list[dict[str, object]] = []

    def fake_post(
        url,
        *,
        json,
        timeout,
    ):
        calls.append(
            {
                "url": url,
                "json": json,
                "timeout": timeout,
            }
        )

        return FakeResponse()

    result = send_telegram_alert(
        dashboard_data=DASHBOARD_DATA,
        bot_token="test-token",
        chat_id="123456",
        post=fake_post,
    )

    assert result == {
        "success": True,
        "chat_id": "123456",
        "coins": 2,
    }

    assert len(
        calls,
    ) == 1

    assert calls[0]["url"] == (
        "https://api.telegram.org/"
        "bottest-token/sendMessage"
    )

    assert calls[0]["json"]["chat_id"] == (
        "123456"
    )

    assert "BTC" in calls[0]["json"]["text"]

    assert calls[0]["timeout"] == 15


def test_should_reject_missing_bot_token():
    """
    Bot token is required.
    """

    with pytest.raises(
        RuntimeError,
        match=(
            "TELEGRAM_BOT_TOKEN is not configured"
        ),
    ):
        send_telegram_alert(
            dashboard_data=DASHBOARD_DATA,
            bot_token="",
            chat_id="123456",
        )


def test_should_reject_missing_chat_id():
    """
    Chat ID is required.
    """

    with pytest.raises(
        RuntimeError,
        match=(
            "TELEGRAM_CHAT_ID is not configured"
        ),
    ):
        send_telegram_alert(
            dashboard_data=DASHBOARD_DATA,
            bot_token="test-token",
            chat_id="",
        )