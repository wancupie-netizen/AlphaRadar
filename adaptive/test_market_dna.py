from market_dna import build_market_dna


def print_result(title, dna):
    print("=" * 60)
    print(title)
    print(f"DNA         : {dna.dna}")
    print(f"Fingerprint : {dna.hash}")
    print(f"Features    : {dna.features}")
    print()


# ----------------------------------------------------
# TEST 1
# Same Input -> Same Fingerprint
# ----------------------------------------------------

context = {
    "trend": "UPTREND",
    "volatility": "HIGH",
    "volume": "HIGH",
    "liquidity": "GOOD",
    "market_structure": "BREAKOUT",
    "momentum": "STRONG"
}

dna1 = build_market_dna(context)
dna2 = build_market_dna(context)

print_result("TEST 1", dna1)

assert dna1.hash == dna2.hash
assert dna1.dna == dna2.dna

print("✅ TEST 1 PASSED\n")


# ----------------------------------------------------
# TEST 2
# Different Trend
# ----------------------------------------------------

context2 = context.copy()
context2["trend"] = "DOWNTREND"

dna3 = build_market_dna(context2)

print_result("TEST 2", dna3)

assert dna3.hash != dna1.hash

print("✅ TEST 2 PASSED\n")


# ----------------------------------------------------
# TEST 3
# Different Volume
# ----------------------------------------------------

context3 = context.copy()
context3["volume"] = "LOW"

dna4 = build_market_dna(context3)

print_result("TEST 3", dna4)

assert dna4.hash != dna1.hash

print("✅ TEST 3 PASSED\n")


# ----------------------------------------------------
# TEST 4
# Unknown Value
# ----------------------------------------------------

context4 = context.copy()
context4["trend"] = "ABCXYZ"

dna5 = build_market_dna(context4)

print_result("TEST 4", dna5)

assert "UNKNOWN" in dna5.dna

print("✅ TEST 4 PASSED\n")


# ----------------------------------------------------
# TEST 5
# Missing Fields
# ----------------------------------------------------

context5 = {
    "trend": "UPTREND"
}

dna6 = build_market_dna(context5)

print_result("TEST 5", dna6)

assert dna6 is not None

print("✅ TEST 5 PASSED\n")


# ----------------------------------------------------
# TEST 6
# DNA Format
# ----------------------------------------------------

parts = dna1.dna.split("-")

assert len(parts) == 6

print("✅ TEST 6 PASSED\n")


print("=" * 60)
print("🎉 ALL MARKET DNA TESTS PASSED")
print("=" * 60)