"""
History Repository Engineering Test
"""

from datetime import datetime, timezone
from pprint import pprint

from adaptive.compiler.experience_compiler import (
    compile_experience,
)

from adaptive.history.history_repository import (
    save,
    find,
    all_experiences,
    clear,
)


print()

print("=" * 60)
print("History Repository Test")
print("=" * 60)

# --------------------------------------------------
# Clear Repository
# --------------------------------------------------

clear()

print()

print("Repository Cleared")
print("-" * 60)

print(
    "Repository Size :",
    len(
        all_experiences(),
    ),
)

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

# --------------------------------------------------
# Save
# --------------------------------------------------

save(
    experience_1,
)

save(
    experience_2,
)

print()

print("Saved")
print("-" * 60)

print(
    "Repository Size :",
    len(
        all_experiences(),
    ),
)

# --------------------------------------------------
# Find
# --------------------------------------------------

history = find(
    "WATCH|ACCUMULATION",
)

print()

print("History")
print("-" * 60)

for item in history:

    pprint(
        item,
    )

# --------------------------------------------------
# Assertions
# --------------------------------------------------

assert len(history) == 2

assert history[0].fingerprint == "WATCH|ACCUMULATION"

assert history[1].fingerprint == "WATCH|ACCUMULATION"

assert history[0].success_count == 1

assert history[1].failure_count == 1

assert len(all_experiences()) == 1

# --------------------------------------------------
# Clear Again
# --------------------------------------------------

clear()

print()

print("Repository Cleared Again")
print("-" * 60)

print(
    "Repository Size :",
    len(
        all_experiences(),
    ),
)

assert len(
    all_experiences(),
) == 0

print()

print("PASS")