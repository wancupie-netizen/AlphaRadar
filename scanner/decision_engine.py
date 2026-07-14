"""
AlphaRadar Decision Engine

Convert market interpretations into actionable decisions.

Responsibilities
----------------
- Evaluate market interpretations
- Produce a recommendation
- Preserve reasoning

This module does NOT:
- generate narratives
- execute trades
- predict prices
"""

from scanner.decision_types import (
    DecisionType,
    DECISION_PRIORITY,
    DECISION_CONFIDENCE,
)

from scanner.interpretation_types import InterpretationType

# --------------------------------------------------
# Decision Rules
# --------------------------------------------------

DECISION_RULES = {

    # Strong Opportunities
    InterpretationType.STRONG_MOMENTUM:
        DecisionType.ALERT,

    InterpretationType.EARLY_MOMENTUM:
        DecisionType.WATCH,

    InterpretationType.ACCUMULATION:
        DecisionType.WATCH,

    # Review Required
    InterpretationType.DISTRIBUTION:
        DecisionType.REVIEW,

    InterpretationType.WEAK_BREAKOUT:
        DecisionType.REVIEW,

    InterpretationType.RISKY_ACTIVITY:
        DecisionType.REVIEW,

    InterpretationType.THIN_BREAKOUT:
        DecisionType.REVIEW,

    InterpretationType.WEAK_MOMENTUM:
        DecisionType.REVIEW,

    # Ignore
    InterpretationType.LOW_ACTIVITY:
        DecisionType.IGNORE,

    InterpretationType.LOW_INTEREST:
        DecisionType.IGNORE,
}


def make_decision(
    interpretations: set[InterpretationType],
) -> dict:
    """
    Produce a market decision from market interpretations.
    """

    candidate_decisions: set[DecisionType] = set()

    for interpretation in interpretations:

        decision = DECISION_RULES.get(interpretation)

        if decision is not None:
            candidate_decisions.add(decision)

    if not candidate_decisions:

        return {
            "decision": DecisionType.IGNORE,
            "confidence": DECISION_CONFIDENCE[DecisionType.IGNORE],
            "reasons": [],
        }

    final_decision = max(
        candidate_decisions,
        key=lambda decision: DECISION_PRIORITY[decision]
    )

    return {
        "decision": final_decision,
        "confidence": DECISION_CONFIDENCE[final_decision],
        "reasons": sorted(
            reason.value
            for reason in interpretations
        ),
    }