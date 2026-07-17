"""
Knowledge Aggregator Test
"""

from pprint import pprint

from core.artifacts.learning_artifact import (
    LearningArtifact,
    LearningMetadata,
)

from core.knowledge.aggregator import (
    build_knowledge,
)


print("=" * 60)
print("Knowledge Aggregator Test")
print("=" * 60)


# ==========================================================
# Learning Artifacts
# ==========================================================

learning = LearningArtifact(

    token="BTC",

    outcome_artifact_id="OUT-TEST",

    learning_status="SUCCESS",

    summary="Learning generated for testing.",

    metadata=LearningMetadata(

        engine_version="1.0.0",

    ),

)


# ==========================================================
# Aggregate
# ==========================================================

knowledge = build_knowledge(

    [learning],

)


# ==========================================================
# Output
# ==========================================================

pprint(knowledge)


# ==========================================================
# Assertions
# ==========================================================

assert knowledge.token == "BTC"

assert knowledge.learning_artifact_id == learning.artifact_id

assert knowledge.sample_size == 1

assert knowledge.success_rate == 100.0

assert knowledge.confidence == "HIGH"

assert knowledge.created_at is not None


print("\nPASS")