from scanner.learning_store import (
    load_latest_learning,
)

print("=" * 60)
print("Learning Store Test")
print("=" * 60)

payload = load_latest_learning("BTC")

print("Payload")
print(payload)

if payload is None:

    print("\nNo LearningArtifact stored yet.")

else:

    print("\nLearning loaded.")

print("\nPASS")