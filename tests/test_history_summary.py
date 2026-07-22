"""
History Summary Engineering Test
"""

from datetime import datetime, timezone
from pprint import pprint

from adaptive.history.history_summary import (
    create_history_summary,
)


print()

print("=" * 60)
print("History Summary Test")
print("=" * 60)

# --------------------------------------------------
# Build History Summary
# --------------------------------------------------

summary = create_history_summary(

    seen_before=True,

    sample_size=27,

    most_common_outcome="CONTINUATION",

    outcome_occurrence=18,

    success_rate=81.48,

    average_duration_hours=18.0,

    last_seen=datetime.now(
        timezone.utc,
    ),

)

print()

pprint(summary)

print()

# --------------------------------------------------
# Assertions
# --------------------------------------------------

assert summary.seen_before is True

assert summary.sample_size == 27

assert summary.most_common_outcome == "CONTINUATION"

assert summary.outcome_occurrence == 18

assert summary.success_rate == 81.48

assert summary.average_duration_hours == 18.0

assert summary.metadata.engine_version == "1.0.0"

print("PASS")