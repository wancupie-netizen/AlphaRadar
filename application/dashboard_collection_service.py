"""
AlphaRadar Dashboard Collection Service

Application orchestration layer
for building dashboard cards
for multiple tokens.

Responsibilities
----------------
- Iterate watchlist
- Build DashboardCard list

This module does NOT:
- access databases
- perform calculations
- perform AI analysis
"""

from datetime import datetime

from adaptive.dashboard.dashboard_card import (
    DashboardCard,
)

from application.adaptive_dashboard_service import (
    build_adaptive_dashboard,
)


# --------------------------------------------------
# Dashboard Collection
# --------------------------------------------------

def build_dashboard_collection(
    *,
    dashboards: list[dict],
) -> list[DashboardCard]:
    """
    Build DashboardCard collection.
    """

    cards = []

    for item in dashboards:

        card = build_adaptive_dashboard(

            token=item["token"],

            fingerprint=item["fingerprint"],

            decision=item["decision"],

            confidence=item["confidence"],

            summary=item["summary"],

            reasons=item["reasons"],

            last_updated=item.get(

                "last_updated",

                datetime.utcnow(),

            ),

        )

        cards.append(
            card,
        )

    return cards