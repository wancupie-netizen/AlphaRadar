"""
Evidence Builder Engineering Test
"""

from datetime import datetime, timezone
from pprint import pprint

from adaptive.compiler.experience_compiler import (
    compile_experience,
)

from adaptive.evidence.evidence_builder import (
    build_evidence,
)


print()

print("=" * 60)
print("Evidence Builder Test")
print("=" * 60)

# --------------------------------------------------
# Build Experience
# --------------------------------------------------

experience = compile_experience(

    fingerprint="WATCH|ACCUMULATION",

    success=True,

    timestamp=datetime.now(
        timezone.utc,
    ),

)

print()

print("Experience")
print("-" * 60)

pprint(experience)

# --------------------------------------------------
# Build Evidence
# --------------------------------------------------

evidence = build_evidence(
    experience,
)

print()

print("Evidence")
print("-" * 60)

pprint(evidence)

# --------------------------------------------------
# Assertions
# --------------------------------------------------

assert evidence.seen_before is True

assert evidence.sample_size == 1

assert evidence.success_rate == 100.0

assert evidence.last_seen == experience.last_seen

assert evidence.metadata.engine_version == "1.0.0"

print()

print("PASS")