"""
Founder MVP Acceptance Tests.

These tests verify the complete Founder MVP user journey.

Production Features Verified

- Multi Coin Dashboard
- Shared Dashboard API
- Telegram Message Builder
- Founder README
"""

from pathlib import Path

from application.founder_dashboard_service import (
    FOUNDER_TOKENS,
)

from application.telegram_notifier import (
    build_telegram_message,
)

from application.founder_dashboard_data import (
    serialize_founder_dashboard_results,
)


# --------------------------------------------------
# Founder Tokens
# --------------------------------------------------

def test_should_support_official_founder_tokens():
    """
    Founder MVP must support the official token list.
    """

    assert FOUNDER_TOKENS == (

        "BTC",

        "ETH",

        "SOL",

        "XRP",

        "SUI",

    )


# --------------------------------------------------
# Shared Dashboard Data
# --------------------------------------------------

def test_should_build_shared_dashboard_data():
    """
    Shared dashboard data should preserve
    Founder token ordering.
    """

    dashboard = serialize_founder_dashboard_results(

        [

            {

                "token": "BTC",

                "card": None,

                "error": "Unavailable",

            },

            {

                "token": "ETH",

                "card": None,

                "error": "Unavailable",

            },

        ]

    )

    assert dashboard[0]["token"] == "BTC"

    assert dashboard[1]["token"] == "ETH"

    assert dashboard[0]["available"] is False

    assert dashboard[1]["available"] is False


# --------------------------------------------------
# Telegram Message
# --------------------------------------------------

def test_should_build_founder_telegram_message():
    """
    Telegram message should contain
    the Founder dashboard snapshot.
    """

    dashboard = [

        {

            "token": "BTC",

            "available": True,

            "decision": "WATCH",

            "confidence": "HIGH",

            "historical_success": 66.67,

            "seen_before": True,

            "reasons": [

                "ACCUMULATION",

            ],

            "summary": "Bullish",

            "error": None,

        }

    ]

    message = build_telegram_message(

        dashboard,

    )

    assert "BTC" in message

    assert "WATCH" in message

    assert "HIGH" in message

    assert "66.67%" in message

    assert "ACCUMULATION" in message


# --------------------------------------------------
# README
# --------------------------------------------------

def test_should_have_founder_readme():
    """
    Founder documentation
    must exist.
    """

    assert Path(

        "README.md",

    ).exists()


# --------------------------------------------------
# Project Launcher
# --------------------------------------------------

def test_should_have_root_launcher():
    """
    Founder MVP should expose
    one simple launcher.
    """

    assert Path(

        "main.py",

    ).exists()