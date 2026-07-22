"""
Experience Artifact Engineering Test
"""

from pprint import pprint
from datetime import datetime, timezone

from adaptive.artifacts.experience_artifact import (
    create_experience,
)


print()

print("=" * 60)
print("Experience Artifact Test")
print("=" * 60)

experience = create_experience(

    fingerprint="WATCH|ACCUMULATION",

    sample_size=18,

    success_count=13,

    failure_count=5,

    success_rate=72.22,

    last_seen=datetime.now(
        timezone.utc,
    ),

)

pprint(experience)

print()

assert experience.experience_id.startswith(
    "EXP-"
)

assert experience.sample_size == 18

assert experience.success_count == 13

assert experience.failure_count == 5

assert experience.success_rate == 72.22

assert experience.metadata.engine_version == "1.0.0"

print("PASS")