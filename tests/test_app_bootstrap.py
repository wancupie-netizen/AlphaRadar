"""
Tests for AlphaRadar Founder MVP FastAPI Application.
"""

from unittest.mock import patch

from fastapi import FastAPI

from app.main import (
    APP_TITLE,
    APP_VERSION,
    HOST,
    PORT,
    app,
    build_current_dashboard_data,
    dashboard_api,
    founder_home,
    health_check,
    telegram_send,
)


def test_should_create_fastapi_application():
    """
    Application should expose FastAPI.
    """

    assert isinstance(
        app,
        FastAPI,
    )

    assert app.title == APP_TITLE

    assert app.version == APP_VERSION


@patch(
    "app.main.render_founder_dashboard"
)
@patch(
    "app.main.build_founder_dashboard_results"
)
def test_should_render_founder_dashboard(
    mock_build_results,
    mock_render_dashboard,
):
    """
    Root route should connect service and presenter.
    """

    results = [
        {
            "token": "BTC",
            "card": None,
            "error": "Test state.",
        }
    ]

    mock_build_results.return_value = results

    mock_render_dashboard.return_value = (
        "<html>Founder Dashboard</html>"
    )

    assert founder_home() == (
        "<html>Founder Dashboard</html>"
    )

    mock_render_dashboard.assert_called_once_with(
        results,
    )


@patch(
    "app.main.serialize_founder_dashboard_results"
)
@patch(
    "app.main.build_founder_dashboard_results"
)
def test_should_build_shared_dashboard_data(
    mock_build_results,
    mock_serialize,
):
    """
    API and Telegram should use shared data.
    """

    results = [
        {
            "token": "BTC",
        }
    ]

    data = [
        {
            "token": "BTC",
            "available": True,
        }
    ]

    mock_build_results.return_value = results

    mock_serialize.return_value = data

    assert build_current_dashboard_data() == data

    mock_serialize.assert_called_once_with(
        results,
    )


@patch(
    "app.main.build_current_dashboard_data"
)
def test_should_return_dashboard_api(
    mock_build_data,
):
    """
    Dashboard API should return shared data.
    """

    data = [
        {
            "token": "BTC",
        }
    ]

    mock_build_data.return_value = data

    assert dashboard_api() == data


@patch(
    "app.main.send_telegram_alert"
)
@patch(
    "app.main.build_current_dashboard_data"
)
def test_should_send_current_snapshot(
    mock_build_data,
    mock_send,
):
    """
    Telegram should receive current shared data.
    """

    data = [
        {
            "token": "BTC",
        }
    ]

    mock_build_data.return_value = data

    mock_send.return_value = {
        "success": True,
        "coins": 1,
    }

    result = telegram_send()

    assert result["success"] is True

    mock_send.assert_called_once_with(
        dashboard_data=data,
    )


def test_should_return_healthy_status():
    """
    Health endpoint should remain available.
    """

    assert health_check() == {
        "status": "ok",
        "application": APP_TITLE,
        "version": APP_VERSION,
    }


def test_should_use_local_server_defaults():
    """
    Founder launch contract remains simple.
    """

    assert HOST == "127.0.0.1"

    assert PORT == 8000