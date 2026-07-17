from scanner.learning_store import (
    load_latest_learning,
)

from scanner.deserializers.learning_deserializer import (
    deserialize_learning,
)

print("=" * 60)
print("Learning Deserializer Test")
print("=" * 60)

payload = load_latest_learning("BTC")

print("Payload")
print(payload)

if payload is None:

    print("\nNo LearningArtifact stored yet.")
    print("\nPASS")

else:

    artifact = deserialize_learning(payload)

    print("\nArtifact")
    print(artifact)

    print("\nPASS")