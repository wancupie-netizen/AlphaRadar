"""
AlphaRadar Founder Dashboard Service.

Runs the existing AlphaRadar engine sequentially for the
Founder MVP token list.

Responsibilities
----------------
- Define the Founder MVP token list
- Run one production scan per token
- Preserve token ordering
- Return successful DashboardCard objects
- Preserve clear error information for unavailable tokens

This module does NOT:
- render HTML
- start FastAPI
- use threading
- use async workers
- send Telegram alerts
- retry scans automatically
"""

from __future__ import annotations

from collections.abc import Callable, Iterable

from presentation.live_dashboard import (
    extract_dashboard,
    normalize_token,
)

from scanner.runner import (
    run_scan,
)


# ==========================================================
# Founder MVP Tokens
# ==========================================================

FOUNDER_TOKENS = (
    "BTC",
    "ETH",
    "SOL",
    "XRP",
    "SUI",
)


# ==========================================================
# Service
# ==========================================================

def build_founder_dashboard_results(
    *,
    tokens: Iterable[str] = FOUNDER_TOKENS,
    scan: Callable[[str], dict] = run_scan,
) -> list[dict[str, object]]:
    """
    Run sequential AlphaRadar scans for Founder MVP tokens.

    Each returned result contains:

    - token
    - card
    - error

    A failed token does not prevent the remaining tokens
    from appearing on the Founder Dashboard.
    """

    results: list[dict[str, object]] = []

    for token in tokens:

        normalized_token = normalize_token(
            token,
        )

        try:

            scan_result = scan(
                normalized_token,
            )

            card = extract_dashboard(
                scan_result,
            )

        except (
            RuntimeError,
            ValueError,
        ) as error:

            results.append(
                {
                    "token": normalized_token,
                    "card": None,
                    "error": str(error),
                }
            )

            continue

        results.append(
            {
                "token": normalized_token,
                "card": card,
                "error": None,
            }
        )

    return results