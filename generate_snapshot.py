"""
AlphaRadar Latest Snapshot Command.

Run from the project root:

    python generate_snapshot.py

The command scans the current CoinMarketCap Top 100 universe
and replaces the latest shared snapshot.
"""

from __future__ import annotations

from application.founder_snapshot_service import (
    generate_latest_snapshot,
)


def main() -> int:
    """
    Generate and report the latest AlphaRadar snapshot.
    """

    print()

    print("=" * 60)
    print("AlphaRadar Top 100 Snapshot")
    print("=" * 60)

    try:

        result = generate_latest_snapshot()

    except Exception as error:

        print()
        print(
            f"Snapshot failed: {error}"
        )
        print()

        return 1

    print()
    print(
        f"Total coins       : {result['total_coins']}"
    )
    print(
        f"Available coins   : {result['available_coins']}"
    )
    print(
        f"Unavailable coins : {result['unavailable_coins']}"
    )
    print(
        f"Generated at      : {result['generated_at']}"
    )
    print(
        f"Snapshot file     : {result['snapshot_file']}"
    )
    print()

    return 0


if __name__ == "__main__":

    raise SystemExit(
        main()
    )