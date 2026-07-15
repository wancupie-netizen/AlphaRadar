"""
AlphaRadar Validation Suite

Entry point for all engineering validation.

Version:
    v0.7.2-alpha
"""

from validation.smoke_test import run as run_smoke
from validation.core_engine_test import run as run_pipeline


def print_header():

    print()
    print("=" * 50)
    print("AlphaRadar Validation Suite")
    print("=" * 50)
    print("Version : v0.7.2-alpha")
    print()


def print_summary(results):

    print()
    print("=" * 50)
    print("Validation Summary")
    print("=" * 50)

    overall_pass = True

    for result in results:

        print(f"{result['name']:<25} {result['status']}")

        if result["status"] != "PASS":
            overall_pass = False

    print("-" * 50)

    if overall_pass:
        print("Overall Status : PASS")
        print("Engine Status  : VERIFIED")
    else:
        print("Overall Status : FAIL")
        print("Engine Status  : VALIDATION FAILED")

    print("=" * 50)


def main():

    print_header()

    results = []

    smoke = run_smoke()
    results.append(smoke)

    if smoke["status"] == "PASS":

        pipeline = run_pipeline()
        results.append(pipeline)

    print_summary(results)


if __name__ == "__main__":
    main()