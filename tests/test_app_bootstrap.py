"""
Tests for AlphaRadar Founder MVP FastAPI Bootstrap.
"""

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


# ==========================================================
# Application Contract
# ==========================================================

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


# ==========================================================
# Founder Home
# ==========================================================

def test_should_render_founder_home():
    """
    Root page should clearly confirm that AlphaRadar is running.
    """

    html = founder_home()

    assert "<!DOCTYPE html>" in html

    assert "AlphaRadar" in html

    assert "Founder MVP" in html

    assert "running" in html

    assert "Multi-coin intelligence dashboard" in html


# ==========================================================
# Health Check
# ==========================================================

def test_should_return_healthy_application_status():
    """
    Health route should expose a minimal readiness response.
    """

    result = health_check()

    assert result == {
        "status": "ok",
        "application": APP_TITLE,
        "version": APP_VERSION,
    }


# ==========================================================
# Local Server Configuration
# ==========================================================

def test_should_use_founder_local_server_defaults():
    """
    Local launch contract must remain simple for founders.
    """

    assert HOST == "127.0.0.1"

    assert PORT == 8000