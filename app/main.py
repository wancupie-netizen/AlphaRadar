"""
AlphaRadar Founder MVP FastAPI Application.

Run from the project root:

    python app/main.py

Then open:

    http://127.0.0.1:8000

Responsibilities
----------------
- Create the FastAPI application
- Build the Founder multi-coin dashboard
- Expose the application health endpoint
- Start the local Uvicorn server

This module does NOT:
- calculate market decisions
- access persistence directly
- send Telegram alerts
- use background workers
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from application.founder_dashboard_service import (
    build_founder_dashboard_results,
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