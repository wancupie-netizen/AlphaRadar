"""
AlphaRadar Dashboard Theme.

Centralised visual language for every Dashboard presenter.

Responsibilities
----------------
- Dashboard colour palette
- Typography
- Card spacing
- Badge colours
- Shared CSS

This module does NOT:
- render HTML
- access DashboardCard
- calculate values
"""

from __future__ import annotations


# ==========================================================
# Theme
# ==========================================================

THEME = {

    "background": "#0f172a",

    "surface": "#1e293b",

    "surface_alt": "#334155",

    "text": "#f8fafc",

    "muted": "#94a3b8",

    "border": "#475569",

    "buy": "#22c55e",

    "watch": "#3b82f6",

    "sell": "#ef4444",

    "unknown": "#64748b",

}


# ==========================================================
# Decision Colours
# ==========================================================

_DECISION_COLOURS = {

    "BUY": THEME["buy"],

    "WATCH": THEME["watch"],

    "SELL": THEME["sell"],

}


def decision_colour(
    decision: str,
) -> str:
    """
    Return dashboard colour for a decision.
    """

    return _DECISION_COLOURS.get(

        decision.upper(),

        THEME["unknown"],

    )


# ==========================================================
# Shared CSS
# ==========================================================

def build_dashboard_css() -> str:
    """
    Shared AlphaRadar Dashboard CSS.
    """

    return f"""
body {{

    margin:0;

    background:{THEME["background"]};

    color:{THEME["text"]};

    font-family:
        Inter,
        Segoe UI,
        Arial,
        sans-serif;

}}

.container {{

    max-width:1200px;

    margin:40px auto;

    padding:24px;

}}

.card {{

    background:{THEME["surface"]};

    border:1px solid {THEME["border"]};

    border-radius:16px;

    padding:24px;

    margin-bottom:24px;

}}

.badge {{

    display:inline-block;

    padding:8px 16px;

    border-radius:999px;

    font-weight:bold;

}}

h1,h2,h3 {{

    margin-top:0;

}}

small {{

    color:{THEME["muted"]};

}}
"""