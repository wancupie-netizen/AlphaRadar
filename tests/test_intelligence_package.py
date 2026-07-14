"""
Tests for IntelligencePackage.
"""

from scanner.models import (
    IntelligencePackage,
    KnowledgeSummary,
    KnowledgeContext,
    ExplanationResult,
)


def test_should_create_intelligence_package():

    summary = KnowledgeSummary(

        total_events=1,

        latest_decision="WATCH",

        latest_confidence="MEDIUM",

        decision_frequency={

            "WATCH": 1,

        },

        most_common_decision="WATCH",

    )

    context = KnowledgeContext(

        history=[],

        summary=summary,

        patterns=[],

        trend=None,

    )

    explanation = ExplanationResult(

        summary="Momentum improving.",

        recommendation="Continue monitoring.",

        highlights=[],

    )

    package = IntelligencePackage(

        token="BTC",

        observation={},

        signals=[],

        interpretations=[],

        decision={

            "decision": "WATCH",

            "confidence": "MEDIUM",

            "reasons": [],

        },

        context=context,

        explanation=explanation,

    )

    assert package.token == "BTC"

    assert package.context is context

    assert package.explanation is explanation