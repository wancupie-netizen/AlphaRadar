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
    founder_home,
    health_check,
)


def test_should_create_fastapi_application():
    """
    Bootstrap should expose one valid FastAPI application.
    """

    assert isinstance(
        app,
        FastAPI,
    )

    assert app.title == APP_TITLE

    assert app.version == APP_VERSION


def test_should_disable_public_documentation():
    """
    Founder MVP does not need public API documentation.
    """

    assert app.docs_url is None

    assert app.redoc_url is None


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
    Root route should connect service to presenter.
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

    html = founder_home()

    assert html == (
        "<html>Founder Dashboard</html>"
    )

    mock_build_results.assert_called_once_with()

    mock_render_dashboard.assert_called_once_with(
        results,
    )


def test_should_return_healthy_application_status():
    """
    Health route should expose readiness response.
    """

    result = health_check()

    assert result == {
        "status": "ok",
        "application": APP_TITLE,
        "version": APP_VERSION,
    }


def test_should_use_founder_local_server_defaults():
    """
    Local launch contract must remain simple.
    """

    assert HOST == "127.0.0.1"

    assert PORT == 8000