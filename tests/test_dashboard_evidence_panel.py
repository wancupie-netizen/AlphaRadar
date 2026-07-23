"""
Tests for Dashboard Evidence Panel.
"""

import pytest

from presentation.dashboard_components.evidence_panel import (
    normalize_reasons,
    render_evidence_panel,
)


# ==========================================================
# Normalization
# ==========================================================

def test_should_normalize_reason_list():

    reasons = normalize_reasons(

        [

            " Breakout ",

            "",

            "Liquidity",

            "   ",

            "Momentum",

        ]

    )

    assert reasons == [

        "Breakout",

        "Liquidity",

        "Momentum",

    ]


def test_should_reject_non_list():

    with pytest.raises(

        ValueError,

        match="Reasons must be a list",

    ):

        normalize_reasons(

            "Breakout",

        )


def test_should_reject_non_string_reason():

    with pytest.raises(

        ValueError,

        match="Every reason must be a string",

    ):

        normalize_reasons(

            [

                "Breakout",

                123,

            ]

        )


# ==========================================================
# Renderer
# ==========================================================

def test_should_render_evidence_list():

    html = render_evidence_panel(

        reasons=[

            "Accumulation",

            "Liquidity",

            "Breakout",

        ],

    )

    assert "Evidence" in html

    assert "Accumulation" in html

    assert "Liquidity" in html

    assert "Breakout" in html

    assert "evidence-list" in html


def test_should_escape_html():

    html = render_evidence_panel(

        reasons=[

            "<script>",

        ],

    )

    assert "<script>" not in html

    assert "&lt;script&gt;" in html


def test_should_render_empty_state():

    html = render_evidence_panel(

        reasons=[],

    )

    assert "No supporting evidence available." in html

    assert "empty-state" in html