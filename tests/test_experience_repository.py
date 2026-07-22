"""
Experience Repository Engineering Test
"""

from datetime import datetime, timezone
from pprint import pprint

from adaptive.compiler.experience_compiler import (
    compile_experience,
)

from adaptive.repository.experience_repository import (
    save_experience,
    load_experience,
    experience_exists,
    clear_repository,
    repository_size,
)


print()

print("=" * 60)
print("Experience Repository Test")
print("=" * 60)

# --------------------------------------------------
# Clean Repository
# --------------------------------------------------

clear_repository()

assert repository_size() == 0

print()

print("Repository Cleared")
print("-" * 60)

print("Repository Size :", repository_size())

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

print("Experience Built")
print("-" * 60)

pprint(experience)

# --------------------------------------------------
# Save
# --------------------------------------------------

save_experience(
    experience,
)

print()

print("Saved")
print("-" * 60)

assert repository_size() == 1

assert experience_exists(
    "WATCH|ACCUMULATION"
)

print("Repository Size :", repository_size())

# --------------------------------------------------
# Load
# --------------------------------------------------

loaded = load_experience(
    "WATCH|ACCUMULATION"
)

print()

print("Loaded")
print("-" * 60)

pprint(loaded)

assert loaded is not None

assert loaded.fingerprint == "WATCH|ACCUMULATION"

assert loaded.sample_size == 1

assert loaded.success_count == 1

assert loaded.failure_count == 0

assert loaded.success_rate == 100.0

# --------------------------------------------------
# Clear Again
# --------------------------------------------------

clear_repository()

print()

print("Repository Cleared Again")
print("-" * 60)

assert repository_size() == 0

assert not experience_exists(
    "WATCH|ACCUMULATION"
)

print("Repository Size :", repository_size())

print()

print("PASS")