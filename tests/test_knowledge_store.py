from scanner.knowledge_store import (
    load_latest_knowledge,
)

print("=" * 60)
print("Knowledge Store Test")
print("=" * 60)

payload = load_latest_knowledge("BTC")

print("Payload")
print(payload)

if payload is None:

    print("\nNo KnowledgeArtifact stored yet.")
    print("\nPASS")

else:

    print("\nKnowledge loaded.")
    print("\nPASS")