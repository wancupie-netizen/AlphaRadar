from adaptive.identity.decision_fingerprint import (
    generate_decision_fingerprint,
)

from scanner.decision_types import DecisionType
from scanner.signal_types import SignalType
from scanner.interpretation_types import InterpretationType


def test_same_input_returns_same_fingerprint():

    fp1 = generate_decision_fingerprint(
        DecisionType.ALERT,
        ["Volume Up", "Liquidity Up"],
        [
            SignalType.VOLUME_UP,
            SignalType.LIQUIDITY_UP,
        ],
        [
            InterpretationType.STRONG_MOMENTUM,
        ],
    )

    fp2 = generate_decision_fingerprint(
        DecisionType.ALERT,
        ["Liquidity Up", "Volume Up"],
        [
            SignalType.LIQUIDITY_UP,
            SignalType.VOLUME_UP,
        ],
        [
            InterpretationType.STRONG_MOMENTUM,
        ],
    )

    assert fp1 == fp2


def test_different_decision_returns_different_fingerprint():

    fp1 = generate_decision_fingerprint(
        DecisionType.ALERT,
        [],
        [],
        [],
    )

    fp2 = generate_decision_fingerprint(
        DecisionType.WATCH,
        [],
        [],
        [],
    )

    assert fp1 != fp2


def test_returns_sha256_hex():

    fp = generate_decision_fingerprint(
        DecisionType.ALERT,
        [],
        [],
        [],
    )

    assert isinstance(fp, str)
    assert len(fp) == 64