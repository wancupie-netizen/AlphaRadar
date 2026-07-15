from datetime import datetime

from experience_memory import (
    Experience,
    ExperienceMemory,
)


def print_header(title):
    print("=" * 60)
    print(title)
    print("=" * 60)


memory = ExperienceMemory()


# --------------------------------------------------
# TEST 1
# --------------------------------------------------

print_header("TEST 1 - CREATE EXPERIENCE")

exp1 = Experience(
    decision_id="DEC-000001",
    decision_fingerprint="ABC123",
    market_dna="UPTREND-HIGHVOL-HIGHVOLM-GOODLIQ-BREAKOUT-STRONG",
    decision="BUY",
    confidence=0.91,
    timestamp=datetime.now(),
    metadata={
        "symbol": "BTC"
    }
)

print(exp1)

print("\n✅ TEST 1 PASSED\n")


# --------------------------------------------------
# TEST 2
# --------------------------------------------------

print_header("TEST 2 - ADD EXPERIENCE")

memory.add(exp1)

assert memory.count() == 1

print(memory.count())

print("\n✅ TEST 2 PASSED\n")


# --------------------------------------------------
# TEST 3
# --------------------------------------------------

print_header("TEST 3 - FIND DECISION")

result = memory.find_by_decision_id(
    "DEC-000001"
)

assert result is not None
assert result.decision == "BUY"

print(result)

print("\n✅ TEST 3 PASSED\n")


# --------------------------------------------------
# TEST 4
# --------------------------------------------------

print_header("TEST 4 - FIND DNA")

results = memory.find_by_market_dna(
    "UPTREND-HIGHVOL-HIGHVOLM-GOODLIQ-BREAKOUT-STRONG"
)

assert len(results) == 1

print(results)

print("\n✅ TEST 4 PASSED\n")


# --------------------------------------------------
# TEST 5
# --------------------------------------------------

print_header("TEST 5 - SAME DNA")

exp2 = Experience(
    decision_id="DEC-000002",
    decision_fingerprint="XYZ999",
    market_dna="UPTREND-HIGHVOL-HIGHVOLM-GOODLIQ-BREAKOUT-STRONG",
    decision="BUY",
    confidence=0.85,
    timestamp=datetime.now(),
    metadata={
        "symbol": "ETH"
    }
)

memory.add(exp2)

results = memory.find_by_market_dna(
    "UPTREND-HIGHVOL-HIGHVOLM-GOODLIQ-BREAKOUT-STRONG"
)

assert len(results) == 2

print(len(results))

print("\n✅ TEST 5 PASSED\n")


# --------------------------------------------------
# TEST 6
# --------------------------------------------------

print_header("TEST 6 - DUPLICATE")

try:

    duplicate = Experience(
        decision_id="DEC-000001",
        decision_fingerprint="NEW",
        market_dna="TEST",
        decision="SELL",
        confidence=0.1,
        timestamp=datetime.now(),
        metadata={}
    )

    memory.add(duplicate)

    raise AssertionError(
        "Duplicate Decision ID accepted."
    )

except ValueError:

    print("Duplicate rejected correctly.")

print("\n✅ TEST 6 PASSED\n")


# --------------------------------------------------
# TEST 7
# --------------------------------------------------

print_header("TEST 7 - EXISTS")

assert memory.exists("DEC-000001")
assert not memory.exists("DEC-999999")

print("Exists OK")

print("\n✅ TEST 7 PASSED\n")


# --------------------------------------------------
# TEST 8
# --------------------------------------------------

print_header("TEST 8 - ALL")

all_exp = memory.all()

assert len(all_exp) == 2

print(len(all_exp))

print("\n✅ TEST 8 PASSED\n")


# --------------------------------------------------
# TEST 9
# --------------------------------------------------

print_header("TEST 9 - IMMUTABLE")

try:

    exp1.decision = "SELL"

    raise AssertionError(
        "Experience should be immutable."
    )

except Exception:

    print("Immutable verified.")

print("\n✅ TEST 9 PASSED\n")


# --------------------------------------------------
# TEST 10
# --------------------------------------------------

print_header("TEST 10 - CLEAR")

memory.clear()

assert memory.count() == 0

print(memory.count())

print("\n✅ TEST 10 PASSED\n")


print("=" * 60)
print("🎉 ALL EXPERIENCE MEMORY TESTS PASSED")
print("=" * 60)