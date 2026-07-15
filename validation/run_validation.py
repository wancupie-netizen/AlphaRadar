"""
AlphaRadar Validation Suite

Entry point for all engineering validation.

Version:
    v0.8.0-alpha
"""

from pathlib import Path
import sys

# ==========================================================
# Ensure Project Root
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# ==========================================================
# Validation Modules
# ==========================================================

from validation.smoke_test import run as run_smoke
from validation.decision_gate_test import run as run_decision_gate
from validation.regression_test import run as run_regression


# ==========================================================
# UI
# ==========================================================

def print_header():

    print()
    print("=" * 60)
    print("AlphaRadar Validation Suite")
    print("=" * 60)
    print("Version : v0.8.0-alpha")
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


# ==========================================================
# Main
# ==========================================================

def main():

    print_header()

    results = []

    # ------------------------------------------------------
    # Smoke Test
    # ------------------------------------------------------

    smoke = run_smoke()
    results.append(smoke)

    if smoke["status"] != "PASS":

        print_summary(results)
        return

    # ------------------------------------------------------
    # Decision Gate Test
    # ------------------------------------------------------

    try:

        decision_gate = run_decision_gate()
        results.append(decision_gate)

    except Exception as e:

        print("[FAIL] Decision Gate Test")
        print(f"       {e}")

        results.append(
            {
                "name": "Decision Gate Test",
                "status": "FAIL",
                "passed": 0,
                "failed": 1,
                "details": [str(e)],
            }
        )

        print_summary(results)
        return

    if decision_gate["status"] != "PASS":

        print_summary(results)
        return

    # ------------------------------------------------------
    # Regression Test
    # ------------------------------------------------------

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