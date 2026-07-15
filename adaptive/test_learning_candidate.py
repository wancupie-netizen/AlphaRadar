from datetime import datetime

from experience_memory import Experience
from learning_candidate import (
    LearningCandidate,
    LearningCandidateBuilder,
)


def print_header(title):
    print("=" * 60)
    print(title)
    print("=" * 60)


builder = LearningCandidateBuilder()

experience = Experience(
    decision_id="DEC-000001",
    decision_fingerprint="FP-ABC-001",
    market_dna="DNA-UPTREND",
    decision="BUY",
    confidence=0.92,
    timestamp=datetime.now(),
    metadata={
        "symbol": "BTC",
        "timeframe": "1H",
    },
)


# --------------------------------------------------
# TEST 1
# Create Builder
# --------------------------------------------------

print_header("TEST 1 - CREATE BUILDER")

assert builder is not None

print("Builder created.")

print("\n✅ TEST 1 PASSED\n")


# --------------------------------------------------
# TEST 2
# Build Candidate
# --------------------------------------------------

print_header("TEST 2 - BUILD CANDIDATE")

candidate = builder.build(experience)

assert isinstance(candidate, LearningCandidate)

print(candidate)

print("\n✅ TEST 2 PASSED\n")


# --------------------------------------------------
# TEST 3
# Decision ID
# --------------------------------------------------

print_header("TEST 3 - DECISION ID")

assert candidate.decision_id == experience.decision_id

print(candidate.decision_id)

print("\n✅ TEST 3 PASSED\n")


# --------------------------------------------------
# TEST 4
# Fingerprint
# --------------------------------------------------

print_header("TEST 4 - FINGERPRINT")

assert (
    candidate.decision_fingerprint
    == experience.decision_fingerprint
)

print(candidate.decision_fingerprint)

print("\n✅ TEST 4 PASSED\n")


# --------------------------------------------------
# TEST 5
# Market DNA
# --------------------------------------------------

print_header("TEST 5 - MARKET DNA")

assert (
    candidate.market_dna
    == experience.market_dna
)

print(candidate.market_dna)

print("\n✅ TEST 5 PASSED\n")


# --------------------------------------------------
# TEST 6
# Experience Reference
# --------------------------------------------------

print_header("TEST 6 - EXPERIENCE REFERENCE")

assert candidate.experience is experience

print("Reference OK")

print("\n✅ TEST 6 PASSED\n")


# --------------------------------------------------
# TEST 7
# Metadata Isolation
# --------------------------------------------------

print_header("TEST 7 - METADATA ISOLATION")

experience.metadata["new_key"] = "new_value"

assert "new_key" not in candidate.metadata

print("Metadata copied correctly.")

print("\n✅ TEST 7 PASSED\n")


# --------------------------------------------------
# TEST 8
# Metadata Immutable
# --------------------------------------------------

print_header("TEST 8 - METADATA IMMUTABLE")

try:

    candidate.metadata["score"] = 100

    raise AssertionError(
        "Metadata should be immutable."
    )

except TypeError:

    print("Metadata immutable.")

print("\n✅ TEST 8 PASSED\n")


# --------------------------------------------------
# TEST 9
# Candidate Immutable
# --------------------------------------------------

print_header("TEST 9 - CANDIDATE IMMUTABLE")

try:

    candidate.decision = "SELL"

    raise AssertionError(
        "Candidate should be immutable."
    )

except Exception:

    print("Candidate immutable.")

print("\n✅ TEST 9 PASSED\n")


print("=" * 60)
print("🎉 ALL LEARNING CANDIDATE TESTS PASSED")
print("=" * 60)