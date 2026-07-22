"""
Evidence Artifact Engineering Test
"""

from pprint import pprint
from datetime import datetime, timezone

from adaptive.artifacts.evidence_artifact import (
    create_evidence,
)


print()

print("=" * 60)
print("Evidence Artifact Test")
print("=" * 60)

evidence = create_evidence(

    seen_before=True,

    sample_size=27,

    success_rate=81.48,

    last_seen=datetime.now(
        timezone.utc,
    ),

)

pprint(evidence)

print()

assert evidence.seen_before is True

assert evidence.sample_size == 27

assert evidence.success_rate == 81.48

assert evidence.last_seen is not None

assert evidence.metadata.engine_version == "1.0.0"

print("PASS")