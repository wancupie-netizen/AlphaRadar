"""
Smoke Test

Verifies that all core AlphaRadar modules
can be imported successfully.

No network calls.

No database calls.

No business logic.
"""

from importlib import import_module


MODULES = {

    "Scanner Engine": "scanner.runner",

    "Observation Builder": "engines.observation_builder",

    "Signal Detector": "engines.signal_detector",

    "Interpretation Engine": "engines.interpretation_engine",

    "Decision Engine": "engines.decision_engine",

    "Knowledge Store": "knowledge.store",

}


def run():

    passed = 0
    failed = 0

    details = []

    print("Running Smoke Test...\n")

    for name, module in MODULES.items():

        try:

            import_module(module)

            print(f"[PASS] {name}")

            details.append(name)

            passed += 1

        except Exception as e:

            print(f"[FAIL] {name}")

            print(f"       {e}")

            failed += 1

    print()

    status = "PASS" if failed == 0 else "FAIL"

    return {

        "name": "Smoke Test",

        "status": status,

        "passed": passed,

        "failed": failed,

        "details": details,

    }