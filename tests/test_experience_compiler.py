"""
Experience Compiler Engineering Test
"""

from pprint import pprint
from datetime import datetime, timezone

from adaptive.compiler.experience_compiler import (
    compile_experience,
)


print()

print("=" * 60)
print("Experience Compiler Test")
print("=" * 60)

timestamp = datetime.now(
    timezone.utc,
)

# --------------------------------------------------
# Success Case
# --------------------------------------------------

experience = compile_experience(

    fingerprint="WATCH|ACCUMULATION",

    success=True,

    timestamp=timestamp,

)

print()

print("SUCCESS CASE")
print("-" * 60)

pprint(experience)

assert experience.sample_size == 1

assert experience.success_count == 1

assert experience.failure_count == 0

assert experience.success_rate == 100.0

assert experience.fingerprint == "WATCH|ACCUMULATION"

# --------------------------------------------------
# Failure Case
# --------------------------------------------------

experience = compile_experience(

    fingerprint="WATCH|ACCUMULATION",

    success=False,

    timestamp=timestamp,

)

print()

print("FAILURE CASE")
print("-" * 60)

pprint(experience)

assert experience.sample_size == 1

assert experience.success_count == 0

assert experience.failure_count == 1

assert experience.success_rate == 0.0

assert experience.fingerprint == "WATCH|ACCUMULATION"

print()

print("PASS")