"""
AlphaRadar Validation Suite

Entry point for all engineering validation.

Version:
    v0.7.2-alpha
"""

from pathlib import Path
import sys

# --------------------------------------------------
# Ensure project root is available on sys.path
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# --------------------------------------------------
# Validation Modules
# --------------------------------------------------

from validation.smoke_test import run as run_smoke
from validation.regression_test import run as run_regression


def print_header():

    print()
    print("=" * 60)
    print("AlphaRadar Validation Suite")
    print("=" * 60)
    print("Version : v0.7.2-alpha")
    print()


def print_summary(results):

    print()
    print("=" * 60)
    print("Validation Summary")
    print("=" * 60)

    overall_pass = True

    for result in results:

        print(f"{result['name']:<30} {result['status']}")

        if result["status"] != "PASS":
            overall_pass = False

    print("-" * 60)

    if overall_pass:
        print("Overall Status : PASS")
        print("Engine Status  : VERIFIED")
    else:
        print("Overall Status : FAIL")
        print("Engine Status  : VALIDATION FAILED")

    print("=" * 60)


def main():

    print_header()

    results = []

    # --------------------------------------------------
    # Smoke Test
    # --------------------------------------------------

    smoke = run_smoke()
    results.append(smoke)

    # --------------------------------------------------
    # Regression Test
    # --------------------------------------------------

    if smoke["status"] == "PASS":

        try:

            regression = run_regression()
            results.append(regression)

        except Exception as e:

            print("[FAIL] Regression Test")
            print(f"       {e}")

            results.append(
                {
                    "name": "Regression Test",
                    "status": "FAIL",
                    "passed": 0,
                    "failed": 1,
                    "details": [str(e)],
                }
            )

    print_summary(results)


if __name__ == "__main__":
    main()