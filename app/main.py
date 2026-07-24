"""
AlphaRadar Founder MVP FastAPI Bootstrap.

Run from the project root:

    python app/main.py

Then open:

    http://127.0.0.1:8000

Responsibilities
----------------
- Create the FastAPI application
- Expose the Founder MVP root route
- Start the local Uvicorn server

This module does NOT:
- run market scans
- build multi-coin dashboards
- send Telegram alerts
- access persistence directly
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse


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
    Display the Founder MVP bootstrap page.

    The real multi-coin dashboard will replace this temporary
    readiness page in the next module.
    """

    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>AlphaRadar Founder MVP</title>

    <style>
        body {
            display: grid;
            min-height: 100vh;
            margin: 0;
            place-items: center;
            background: #07111f;
            color: #f8fafc;
            font-family: Inter, "Segoe UI", Arial, sans-serif;
        }

        main {
            width: min(560px, calc(100% - 40px));
            padding: 36px;
            border: 1px solid #29415c;
            border-radius: 18px;
            background: #102033;
            text-align: center;
        }

        h1 {
            margin-top: 0;
        }

        p {
            color: #94a3b8;
            line-height: 1.7;
        }

        strong {
            color: #22cdb8;
        }
    </style>
</head>

<body>
    <main>
        <h1>AlphaRadar</h1>

        <p>
            Founder MVP web application is
            <strong>running</strong>.
        </p>

        <p>
            Multi-coin intelligence dashboard is the next
            integration checkpoint.
        </p>
    </main>
</body>
</html>
"""


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