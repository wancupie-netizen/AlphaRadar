"""
History Service Engineering Test
"""

from datetime import datetime, timezone
from pprint import pprint

from adaptive.compiler.experience_compiler import (
    compile_experience,
)

from adaptive.history.history_repository import (
    clear,
    save,
)

from adaptive.history.history_service import (
    build_history,
)


print()

print("=" * 60)
print("History Service Test")
print("=" * 60)

# --------------------------------------------------
# Clear Repository
# --------------------------------------------------

clear()

print()

print("Repository Cleared")
print("-" * 60)

# --------------------------------------------------
# Build Experiences
# --------------------------------------------------

experience_1 = compile_experience(

    fingerprint="WATCH|ACCUMULATION",

    success=True,

    timestamp=datetime.now(
        timezone.utc,
    ),

)

experience_2 = compile_experience(

    fingerprint="WATCH|ACCUMULATION",

    success=True,

    timestamp=datetime.now(
        timezone.utc,
    ),

)

experience_3 = compile_experience(

    fingerprint="WATCH|ACCUMULATION",

    success=False,

    timestamp=datetime.now(
        timezone.utc,
    ),

)

print()

print("Experience #1")
print("-" * 60)

pprint(
    experience_1,
)

print()

print("Experience #2")
print("-" * 60)

pprint(
    experience_2,
)

print()

print("Experience #3")
print("-" * 60)

pprint(
    experience_3,
)

# --------------------------------------------------
# Save
# --------------------------------------------------

save(
    experience_1,
)

save(
    experience_2,
)

save(
    experience_3,
)

# --------------------------------------------------
# Build History
# --------------------------------------------------

summary = build_history(

    "WATCH|ACCUMULATION",

)

print()

print("History Summary")
print("-" * 60)

pprint(
    summary,
)

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