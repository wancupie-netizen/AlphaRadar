from scanner.knowledge_store import (
    load_latest_knowledge,
)

from scanner.deserializers.knowledge_deserializer import (
    deserialize_knowledge,
)

print("=" * 60)
print("Knowledge Deserializer Test")
print("=" * 60)

payload = load_latest_knowledge("BTC")

print("Payload")
print(payload)

if payload is None:

    print("\nNo KnowledgeArtifact stored yet.")
    print("\nPASS")

else:

    artifact = deserialize_knowledge(payload)

    print("\nArtifact")
    print(artifact)

    print("\nPASS")