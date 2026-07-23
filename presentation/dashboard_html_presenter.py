"""
AlphaRadar Dashboard HTML Presenter.

Presentation boundary for converting a DashboardCard
into a complete standalone HTML document.

Responsibilities
----------------
- Receive DashboardCard
- Escape dynamic text safely
- Format timestamps
- Render standalone dashboard HTML

This module does NOT:
- access databases
- access repositories
- build DashboardRequest
- make trading decisions
- write files
- open web browsers
"""

from __future__ import annotations

from datetime import datetime
from html import escape

from adaptive.dashboard.dashboard_card import (
    DashboardCard,
)


# ==========================================================
# Formatting Helpers
# ==========================================================

def _escape_text(
    value: object,
) -> str:
    """
    Convert a value into escaped HTML-safe text.
    """

    return escape(
        str(value),
        quote=True,
    )


def _format_datetime(
    value: datetime,
) -> str:
    """
    Format a datetime for dashboard display.

    Timezone information is retained when available.
    """

    return value.isoformat(
        sep=" ",
        timespec="seconds",
    )


def _format_percentage(
    value: float,
) -> str:
    """
    Format historical success as a percentage.
    """

    return f"{value:.2f}%"


def _decision_class(
    decision: str,
) -> str:
    """
    Return a presentation class for a decision.
    """

    normalized = decision.strip().upper()

    if normalized in {
        "BUY",
        "STRONG_BUY",
    }:
        return "decision-positive"

    if normalized in {
        "SELL",
        "STRONG_SELL",
        "AVOID",
    }:
        return "decision-negative"

    return "decision-neutral"


def _confidence_class(
    confidence: str,
) -> str:
    """
    Return a presentation class for confidence.
    """

    normalized = confidence.strip().upper()

    if normalized == "HIGH":
        return "confidence-high"

    if normalized == "LOW":
        return "confidence-low"

    return "confidence-medium"


def _render_reasons(
    reasons: list[str],
) -> str:
    """
    Render decision reasons as HTML list items.
    """

    if not reasons:

        return (
            '<li class="reason-item reason-empty">'
            "No decision reasons available."
            "</li>"
        )

    return "\n".join(

        (
            '<li class="reason-item">'
            f"{_escape_text(reason)}"
            "</li>"
        )

        for reason in reasons
    )


# ==========================================================
# Dashboard Presenter
# ==========================================================

def render_dashboard_html(
    card: DashboardCard,
) -> str:
    """
    Render a DashboardCard as a standalone HTML document.

    Parameters
    ----------
    card
        DashboardCard to present.

    Returns
    -------
    str
        Complete UTF-8 HTML document.
    """

    token = _escape_text(
        card.token,
    )

    decision = _escape_text(
        card.decision,
    )

    confidence = _escape_text(
        card.confidence,
    )

    summary = _escape_text(
        card.summary,
    )

    historical_success = _format_percentage(
        card.historical_success,
    )

    last_updated = _escape_text(
        _format_datetime(
            card.last_updated,
        )
    )

    generated_at = _escape_text(
        _format_datetime(
            card.metadata.generated_at,
        )
    )

    engine_version = _escape_text(
        card.metadata.engine_version,
    )

    decision_css_class = _decision_class(
        card.decision,
    )

    confidence_css_class = _confidence_class(
        card.confidence,
    )

    seen_before_text = (
        "Seen Before"
        if card.seen_before
        else "New Pattern"
    )

    seen_before_class = (
        "history-known"
        if card.seen_before
        else "history-new"
    )

    reasons_html = _render_reasons(
        card.reasons,
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >
    <title>AlphaRadar Dashboard — {token}</title>

    <style>
        :root {{
            color-scheme: dark;

            --background: #07111f;
            --surface: #0d1b2d;
            --surface-soft: #12243a;
            --border: #213853;

            --text-primary: #f5f8fc;
            --text-secondary: #9db0c8;
            --accent: #35d0ba;

            --positive: #39d98a;
            --negative: #ff667d;
            --neutral: #ffcb57;
        }}

        * {{
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            min-height: 100vh;
            background:
                radial-gradient(
                    circle at top right,
                    rgba(53, 208, 186, 0.12),
                    transparent 34%
                ),
                var(--background);
            color: var(--text-primary);
            font-family:
                Inter,
                system-ui,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                sans-serif;
        }}

        .page-shell {{
            width: min(1100px, calc(100% - 32px));
            margin: 0 auto;
            padding: 40px 0 64px;
        }}

        .topbar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
            margin-bottom: 28px;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        .brand-mark {{
            display: grid;
            place-items: center;
            width: 42px;
            height: 42px;
            border: 1px solid rgba(53, 208, 186, 0.45);
            border-radius: 12px;
            background: rgba(53, 208, 186, 0.1);
            color: var(--accent);
            font-weight: 800;
        }}

        .brand-name {{
            margin: 0;
            font-size: 1.05rem;
            letter-spacing: 0.08em;
        }}

        .brand-label {{
            margin: 2px 0 0;
            color: var(--text-secondary);
            font-size: 0.78rem;
        }}

        .engine-version {{
            color: var(--text-secondary);
            font-size: 0.82rem;
        }}

        .dashboard-card {{
            overflow: hidden;
            border: 1px solid var(--border);
            border-radius: 22px;
            background:
                linear-gradient(
                    145deg,
                    rgba(18, 36, 58, 0.94),
                    rgba(8, 20, 35, 0.98)
                );
            box-shadow: 0 28px 70px rgba(0, 0, 0, 0.35);
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            gap: 24px;
            padding: 30px;
            border-bottom: 1px solid var(--border);
        }}

        .token-label {{
            margin: 0 0 8px;
            color: var(--text-secondary);
            font-size: 0.78rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }}

        .token-name {{
            margin: 0;
            font-size: clamp(2.4rem, 7vw, 4.8rem);
            line-height: 1;
        }}

        .status-column {{
            display: flex;
            flex-wrap: wrap;
            align-content: flex-start;
            justify-content: flex-end;
            gap: 10px;
        }}

        .status-pill {{
            display: inline-flex;
            align-items: center;
            min-height: 34px;
            padding: 7px 13px;
            border: 1px solid var(--border);
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.035);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}

        .decision-positive,
        .confidence-high,
        .history-known {{
            border-color: rgba(57, 217, 138, 0.4);
            color: var(--positive);
        }}

        .decision-negative,
        .confidence-low {{
            border-color: rgba(255, 102, 125, 0.4);
            color: var(--negative);
        }}

        .decision-neutral,
        .confidence-medium,
        .history-new {{
            border-color: rgba(255, 203, 87, 0.4);
            color: var(--neutral);
        }}

        .metrics {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            border-bottom: 1px solid var(--border);
        }}

        .metric {{
            padding: 24px 30px;
            border-right: 1px solid var(--border);
        }}

        .metric:last-child {{
            border-right: 0;
        }}

        .metric-label {{
            margin: 0 0 9px;
            color: var(--text-secondary);
            font-size: 0.76rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }}

        .metric-value {{
            margin: 0;
            font-size: 1.45rem;
            font-weight: 750;
        }}

        .content-grid {{
            display: grid;
            grid-template-columns: minmax(0, 1.4fr) minmax(280px, 0.8fr);
        }}

        .content-section {{
            padding: 30px;
        }}

        .content-section + .content-section {{
            border-left: 1px solid var(--border);
        }}

        .section-title {{
            margin: 0 0 16px;
            font-size: 0.8rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }}

        .summary {{
            margin: 0;
            color: var(--text-primary);
            font-size: 1.08rem;
            line-height: 1.75;
        }}

        .reason-list {{
            display: grid;
            gap: 10px;
            margin: 0;
            padding: 0;
            list-style: none;
        }}

        .reason-item {{
            padding: 12px 14px;
            border: 1px solid var(--border);
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.025);
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}

        .reason-item::before {{
            content: "●";
            margin-right: 10px;
            color: var(--accent);
        }}

        .reason-empty::before {{
            color: var(--text-secondary);
        }}

        .card-footer {{
            display: flex;
            justify-content: space-between;
            gap: 20px;
            padding: 18px 30px;
            border-top: 1px solid var(--border);
            color: var(--text-secondary);
            font-size: 0.76rem;
        }}

        @media (max-width: 760px) {{
            .card-header {{
                flex-direction: column;
            }}

            .status-column {{
                justify-content: flex-start;
            }}

            .metrics {{
                grid-template-columns: 1fr;
            }}

            .metric {{
                border-right: 0;
                border-bottom: 1px solid var(--border);
            }}

            .metric:last-child {{
                border-bottom: 0;
            }}

            .content-grid {{
                grid-template-columns: 1fr;
            }}

            .content-section + .content-section {{
                border-top: 1px solid var(--border);
                border-left: 0;
            }}

            .card-footer {{
                flex-direction: column;
            }}
        }}
    </style>
</head>

<body>
    <main class="page-shell">
        <header class="topbar">
            <div class="brand">
                <div class="brand-mark">AR</div>

                <div>
                    <h1 class="brand-name">ALPHARADAR</h1>
                    <p class="brand-label">
                        Adaptive Intelligence Dashboard
                    </p>
                </div>
            </div>

            <div class="engine-version">
                Engine {engine_version}
            </div>
        </header>

        <article class="dashboard-card">
            <header class="card-header">
                <div>
                    <p class="token-label">Tracked Asset</p>
                    <h2 class="token-name">{token}</h2>
                </div>

                <div class="status-column">
                    <span
                        class="status-pill {decision_css_class}"
                    >
                        {decision}
                    </span>

                    <span
                        class="status-pill {confidence_css_class}"
                    >
                        {confidence} Confidence
                    </span>

                    <span
                        class="status-pill {seen_before_class}"
                    >
                        {seen_before_text}
                    </span>
                </div>
            </header>

            <section class="metrics">
                <div class="metric">
                    <p class="metric-label">
                        Recommended Action
                    </p>

                    <p class="metric-value">
                        {decision}
                    </p>
                </div>

                <div class="metric">
                    <p class="metric-label">
                        Confidence
                    </p>

                    <p class="metric-value">
                        {confidence}
                    </p>
                </div>

                <div class="metric">
                    <p class="metric-label">
                        Historical Success
                    </p>

                    <p class="metric-value">
                        {historical_success}
                    </p>
                </div>
            </section>

            <div class="content-grid">
                <section class="content-section">
                    <h3 class="section-title">
                        Intelligence Summary
                    </h3>

                    <p class="summary">
                        {summary}
                    </p>
                </section>

                <section class="content-section">
                    <h3 class="section-title">
                        Decision Reasons
                    </h3>

                    <ul class="reason-list">
                        {reasons_html}
                    </ul>
                </section>
            </div>

            <footer class="card-footer">
                <span>
                    Last updated: {last_updated}
                </span>

                <span>
                    Dashboard generated: {generated_at}
                </span>
            </footer>
        </article>
    </main>
</body>
</html>
"""