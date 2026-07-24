"""
AlphaRadar Founder Dashboard Service.

Runs the existing AlphaRadar engine sequentially for the
current CoinMarketCap Top 100 universe.

Responsibilities
----------------
- Load the daily Top 100 CoinMarketCap universe
- Run one production scan per token
- Preserve market-cap ranking order
- Return successful DashboardCard objects
- Preserve unavailable-token information

This module does NOT:
- render HTML
- start FastAPI
- use threading
- send Telegram alerts
- schedule scans
- retry failed scans automatically
"""

from __future__ import annotations

from collections.abc import (
    Callable,
    Iterable,
)

from application.coinmarketcap_universe import (
    load_top_100_universe,
)

from presentation.live_dashboard import (
    extract_dashboard,
    normalize_token,
)

from scanner.runner import (
    run_scan,
)


# Kept only as a small local fallback reference.
# The default production flow now loads CoinMarketCap Top 100.
FOUNDER_TOKENS = (
    "BTC",
    "ETH",
    "SOL",
    "XRP",
    "SUI",
)


def build_founder_dashboard_results(
    *,
    tokens: Iterable[str] | None = None,
    scan: Callable[[str], dict] = run_scan,
    universe_loader: Callable[
        [],
        Iterable[str],
    ] = load_top_100_universe,
) -> list[dict[str, object]]:
    """
    Run sequential AlphaRadar scans.

    When tokens are not supplied, the daily CoinMarketCap
    Top 100 universe is loaded automatically.
    """

    resolved_tokens = (
        tokens
        if tokens is not None
        else universe_loader()
    )

    results: list[dict[str, object]] = []

    for token in resolved_tokens:

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
                    "error": str(
                        error,
                    ),
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