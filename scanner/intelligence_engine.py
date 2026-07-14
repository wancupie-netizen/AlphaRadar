"""
AlphaRadar Intelligence Engine

Build a complete Intelligence Package.

Responsibilities
----------------
- Detect signals
- Detect interpretations
- Make decisions
- Return a complete intelligence package

This module does NOT:
- access databases
- save knowledge
- publish notifications
"""

from scanner.signal_detector import detect_signals
from scanner.interpretation_engine import detect_interpretations
from scanner.decision_engine import make_decision


def build_intelligence(
    token: str,
    observation: dict,
) -> dict:
    """
    Build a complete Intelligence Package.
    """

    signals = detect_signals(observation)

    interpretations = detect_interpretations(signals)

    decision = make_decision(interpretations)

    return {
        "token": token,
        "observation": observation,
        "signals": sorted(
            signal.value if hasattr(signal, "value") else signal
            for signal in signals
        ),
        "interpretations": sorted(
            interpretation.value
            if hasattr(interpretation, "value")
            else interpretation
            for interpretation in interpretations
        ),
        "decision": decision,
    }