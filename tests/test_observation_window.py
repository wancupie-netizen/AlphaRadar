"""
Observation Window Test
"""

from core.enums.observation_window import (
    ObservationWindow,
)


print("=" * 60)
print("Observation Window Test")
print("=" * 60)


print(list(ObservationWindow))


assert ObservationWindow.MINUTES_15 == "15M"

assert ObservationWindow.HOUR_1 == "1H"

assert ObservationWindow.HOURS_4 == "4H"

assert ObservationWindow.HOURS_24 == "24H"


print("\nPASS")