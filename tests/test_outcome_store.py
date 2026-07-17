from scanner.outcome_store import (
    load_latest_outcome,
)

print("=" * 60)
print("Outcome Store Test")
print("=" * 60)

payload = load_latest_outcome("BTC")

print("Payload")
print(payload)

if payload is None:

    print("\nNo OutcomeArtifact stored yet.")

else:

    print("\nOutcome loaded.")

print("\nPASS")