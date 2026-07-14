from scanner.signal_detector import detect_signals
from scanner.interpretation_engine import detect_interpretations


observation = {
    "price_change_pct": 0.724,
    "volume_change_pct": 14.102,
    "liquidity_change_pct": 0.1569,
    "market_cap_change_pct": None,
    "fdv_change_pct": None,
}


# ---------------------------------------
# Signal Detection
# ---------------------------------------

signals = detect_signals(observation)

# ---------------------------------------
# Interpretation
# ---------------------------------------

interpretations = detect_interpretations(signals)

# ---------------------------------------
# Output
# ---------------------------------------

print("Observation")
print("-------------------------")
print(observation)

print()

print("Signals")
print("-------------------------")

for signal in sorted(signals):
    print(signal)

print()

print("Interpretations")
print("-------------------------")

for interpretation in sorted(interpretations):
    print(interpretation)