"""
History Builder Engineering Test
"""

from datetime import datetime, timezone
from pprint import pprint

from adaptive.compiler.experience_compiler import (
    compile_experience,
)

from adaptive.history.history_builder import (
    build_history_summary,
)


print()

print("=" * 60)
print("History Builder Test")
print("=" * 60)

# --------------------------------------------------
# Build Experiences
# --------------------------------------------------

experiences = [

    compile_experience(

        fingerprint="WATCH|ACCUMULATION",

        success=True,

        timestamp=datetime.now(
            timezone.utc,
        ),

    ),

    compile_experience(

        fingerprint="WATCH|ACCUMULATION",

        success=True,

        timestamp=datetime.now(
            timezone.utc,
        ),

    ),

    compile_experience(

        fingerprint="WATCH|ACCUMULATION",

        success=False,

        timestamp=datetime.now(
            timezone.utc,
        ),

    ),

]

print()

print("Experiences")
print("-" * 60)

for experience in experiences:

    pprint(
        experience,
    )

# --------------------------------------------------
# Build History Summary
# --------------------------------------------------

summary = build_history_summary(

    experiences,

)

print()

print("History Summary")
print("-" * 60)

pprint(summary)

print()

# --------------------------------------------------
# Assertions
# --------------------------------------------------

assert summary.seen_before is True

assert summary.sample_size == 3

assert summary.most_common_outcome == "SUCCESS"

assert summary.outcome_occurrence == 2

assert summary.success_rate == 66.67

assert summary.average_duration_hours == 0.0

assert summary.metadata.engine_version == "1.0.0"

print("PASS")