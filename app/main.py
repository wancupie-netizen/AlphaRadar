"""
AlphaRadar Founder MVP FastAPI Application.

Official launcher from the project root:

    python main.py

Then open:

    http://127.0.0.1:8000

Responsibilities
----------------
- Display the Founder multi-coin dashboard
- Expose shared dashboard data as JSON
- Send the current dashboard snapshot to Telegram
- Expose application health
- Start the local Uvicorn server

This module does NOT:
- calculate market decisions
- access persistence directly
- poll Telegram
- schedule alerts
- use background workers
"""

from __future__ import annotations

import requests

from fastapi import (
    FastAPI,
    HTTPException,
)
from fastapi.responses import (
    HTMLResponse,
)

from application.founder_dashboard_data import (
    serialize_founder_dashboard_results,
)

from application.founder_dashboard_service import (
    build_founder_dashboard_results,
)

from application.telegram_notifier import (
    send_telegram_alert,
)

from presentation.founder_dashboard_presenter import (
    render_founder_dashboard,
)


APP_TITLE = "AlphaRadar Founder MVP"

APP_VERSION = "0.1.0"

HOST = "127.0.0.1"

PORT = 8000


# ==========================================================
# Application
# ==========================================================

app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    docs_url=None,
    redoc_url=None,
)


# ==========================================================
# Shared Dashboard Data
# ==========================================================

def build_current_dashboard_data() -> list[dict[str, object]]:
    """
    Run the engine and return one shared dashboard snapshot.

    The same serialized structure is used by:

    - Dashboard JSON API
    - Telegram alert
    """

    results = build_founder_dashboard_results()

    return serialize_founder_dashboard_results(
        results,
    )


# ==========================================================
# Routes
# ==========================================================

@app.get(
    "/",
    response_class=HTMLResponse,
)
def founder_home() -> str:
    """
    Run sequential Founder scans and display five coins.
    """

    results = build_founder_dashboard_results()

    return render_founder_dashboard(
        results,
    )


@app.get(
    "/api/dashboard",
)
def dashboard_api() -> list[dict[str, object]]:
    """
    Return the current five-coin engine snapshot as JSON.
    """

    return build_current_dashboard_data()


@app.post(
    "/telegram/send",
)
def telegram_send() -> dict[str, object]:
    """
    Send the current five-coin engine snapshot to Telegram.
    """

    dashboard_data = build_current_dashboard_data()

    try:

        return send_telegram_alert(

            dashboard_data=dashboard_data,

        )

    except RuntimeError as error:

        raise HTTPException(

            status_code=503,

            detail=str(
                error,
            ),

        ) from error

    except requests.RequestException as error:

        raise HTTPException(

            status_code=502,

            detail=(
                "Telegram API request failed: "
                f"{error}"
            ),

        ) from error


@app.get(
    "/health",
)
def health_check() -> dict[str, str]:
    """
    Return a minimal application health response.
    """

    return {
        "status": "ok",
        "application": APP_TITLE,
        "version": APP_VERSION,
    }


# ==========================================================
# Local Entry Point
# ==========================================================

def run() -> None:
    """
    Start the local Founder MVP server.
    """

    import uvicorn

    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
    )


if __name__ == "__main__":
    run()