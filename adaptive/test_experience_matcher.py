from datetime import datetime

from experience_memory import (
    Experience,
    ExperienceMemory,
)

from experience_matcher import (
    ExperienceMatcher,
)


def print_header(title):
    print("=" * 60)
    print(title)
    print("=" * 60)


# --------------------------------------------------
# Setup
# --------------------------------------------------

memory = ExperienceMemory()

matcher = ExperienceMatcher(memory)


exp1 = Experience(
    decision_id="DEC-001",
    decision_fingerprint="FP001",
    market_dna="DNA-A",
    decision="BUY",
    confidence=0.91,
    timestamp=datetime.now(),
    metadata={"symbol": "BTC"},
)

exp2 = Experience(
    decision_id="DEC-002",
    decision_fingerprint="FP002",
    market_dna="DNA-A",
    decision="BUY",
    confidence=0.88,
    timestamp=datetime.now(),
    metadata={"symbol": "ETH"},
)

exp3 = Experience(
    decision_id="DEC-003",
    decision_fingerprint="FP003",
    market_dna="DNA-B",
    decision="SELL",
    confidence=0.72,
    timestamp=datetime.now(),
    metadata={"symbol": "SOL"},
)

memory.add(exp1)
memory.add(exp2)
memory.add(exp3)


# --------------------------------------------------
# TEST 1
# Matcher Creation
# --------------------------------------------------

print_header("TEST 1 - CREATE MATCHER")

assert matcher is not None

print("Matcher created.")

print("\n✅ TEST 1 PASSED\n")


# --------------------------------------------------
# TEST 2
# Exact Match
# --------------------------------------------------

print_header("TEST 2 - EXACT MATCH")

results = matcher.match("DNA-A")

assert len(results) == 2

print(results)

print("\n✅ TEST 2 PASSED\n")


# --------------------------------------------------
# TEST 3
# No Match
# --------------------------------------------------

print_header("TEST 3 - NO MATCH")

results = matcher.match("DNA-X")

assert len(results) == 0

print(results)

print("\n✅ TEST 3 PASSED\n")


# --------------------------------------------------
# TEST 4
# Has Match
# --------------------------------------------------

print_header("TEST 4 - HAS MATCH")

assert matcher.has_match("DNA-A")

assert matcher.has_match("DNA-B")

assert matcher.has_match("DNA-X") is False

print("Has Match OK")

print("\n✅ TEST 4 PASSED\n")


# --------------------------------------------------
# TEST 5
# Count
# --------------------------------------------------

print_header("TEST 5 - COUNT")

assert matcher.count("DNA-A") == 2

assert matcher.count("DNA-B") == 1

assert matcher.count("DNA-X") == 0

print("Count OK")

print("\n✅ TEST 5 PASSED\n")


# --------------------------------------------------
# TEST 6
# Limit
# --------------------------------------------------

print_header("TEST 6 - LIMIT")

results = matcher.match(
    "DNA-A",
    limit=1,
)

assert len(results) == 1

print(results)

print("\n✅ TEST 6 PASSED\n")


# --------------------------------------------------
# TEST 7
# Empty Memory
# --------------------------------------------------

print_header("TEST 7 - EMPTY MEMORY")

empty_memory = ExperienceMemory()

empty_matcher = ExperienceMatcher(
    empty_memory
)

results = empty_matcher.match(
    "DNA-A"
)

assert len(results) == 0

assert empty_matcher.count("DNA-A") == 0

assert empty_matcher.has_match("DNA-A") is False

print("Empty memory OK")

print("\n✅ TEST 7 PASSED\n")


# --------------------------------------------------
# TEST 8
# Returned Object Type
# --------------------------------------------------

print_header("TEST 8 - RETURN TYPE")

results = matcher.match("DNA-A")

assert isinstance(results, list)

assert isinstance(results[0], Experience)

print(type(results))
print(type(results[0]))

print("\n✅ TEST 8 PASSED\n")

# --------------------------------------------------
# TEST 9
# Limit Greater Than Available Results
# --------------------------------------------------

print_header("TEST 9 - LIMIT > AVAILABLE")

results = matcher.match(
    "DNA-A",
    limit=100,
)

assert len(results) == 2

print(results)

print("\n✅ TEST 9 PASSED\n")

print("=" * 60)
print("🎉 ALL EXPERIENCE MATCHER TESTS PASSED")
print("=" * 60)