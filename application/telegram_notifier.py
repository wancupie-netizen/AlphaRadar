"""
AlphaRadar Founder Telegram Notifier.

Formats and sends the current Founder Dashboard snapshot
through the Telegram Bot API.

Environment variables
---------------------
TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID

This module does NOT:
- run market scans
- poll Telegram
- manage Telegram commands
- schedule alerts
- store credentials
"""

from __future__ import annotations

import os
from collections.abc import Callable

import requests


def build_telegram_message(
    dashboard_data: list[dict[str, object]],
) -> str:
    """
    Build one Telegram message from shared dashboard data.
    """

    if not isinstance(
        dashboard_data,
        list,
    ):
        raise ValueError(
            "Dashboard data must be a list."
        )

    lines = [
        "🚨 AlphaRadar Founder Alert",
        "",
        "Five markets. One engine.",
    ]

    for item in dashboard_data:

        token = str(
            item.get(
                "token",
                "UNKNOWN",
            )
        )

        lines.extend(
            [
                "",
                f"🔹 {token}",
            ]
        )

        if not item.get(
            "available",
            False,
        ):
            lines.append(
                "Status: UNAVAILABLE"
            )

            error = item.get(
                "error",
            )

            if error:
                lines.append(
                    f"Reason: {error}"
                )

            continue

        lines.extend(
            [
                (
                    "Decision: "
                    f"{item.get('decision', 'UNKNOWN')}"
                ),
                (
                    "Confidence: "
                    f"{item.get('confidence', 'UNKNOWN')}"
                ),
                (
                    "Historical Success: "
                    f"{float(item.get('historical_success', 0.0)):.2f}%"
                ),
                (
                    "Adaptive Memory: "
                    + (
                        "KNOWN PATTERN"
                        if item.get(
                            "seen_before",
                            False,
                        )
                        else "NEW PATTERN"
                    )
                ),
            ]
        )

        reasons = item.get(
            "reasons",
            [],
        )

        if isinstance(
            reasons,
            list,
        ) and reasons:

            lines.append(
                "Evidence:"
            )

            for reason in reasons[:3]:
                lines.append(
                    f"• {reason}"
                )

        else:
            lines.append(
                "Evidence: None available"
            )

    lines.extend(
        [
            "",
            "AlphaRadar · Engine-driven market intelligence",
        ]
    )

    return "\n".join(
        lines,
    )


def send_telegram_alert(
    *,
    dashboard_data: list[dict[str, object]],
    bot_token: str | None = None,
    chat_id: str | None = None,
    post: Callable[..., object] = requests.post,
) -> dict[str, object]:
    """
    Send the Founder Dashboard snapshot to Telegram.
    """

    resolved_bot_token = (
        bot_token
        or os.getenv(
            "TELEGRAM_BOT_TOKEN",
        )
    )

    resolved_chat_id = (
        chat_id
        or os.getenv(
            "TELEGRAM_CHAT_ID",
        )
    )

    if not resolved_bot_token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is not configured."
        )

    if not resolved_chat_id:
        raise RuntimeError(
            "TELEGRAM_CHAT_ID is not configured."
        )

    message = build_telegram_message(
        dashboard_data,
    )

    url = (
        "https://api.telegram.org/"
        f"bot{resolved_bot_token}/sendMessage"
    )

    response = post(
        url,
        json={
            "chat_id": resolved_chat_id,
            "text": message,
        },
        timeout=15,
    )

    response.raise_for_status()

    return {
        "success": True,
        "chat_id": resolved_chat_id,
        "coins": len(
            dashboard_data,
        ),
    }