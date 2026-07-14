from dotenv import load_dotenv
from supabase import create_client
import os

from scanner.watchlist import load_watchlist
from scanner.runner import run_scan


def main():

    print("🚀 AlphaRadar Starting...")

    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        print("❌ Environment variables not found.")
        return

    create_client(url, key)

    print("✅ Environment Loaded")
    print("✅ Connected to Supabase")
    print("Scanner Ready.")

    tokens = load_watchlist()

    print("\nWatchlist Loaded")
    print(tokens)

    for token in tokens:

        print("\n========================")
        print(f"Scanning {token}")

        result = run_scan(token)

        if not result["success"]:
            print(f"❌ {token}")
            print(result["error"])
            continue

        print("✅ Market Event Saved")

        # ---------------------------------------
        # Observation
        # ---------------------------------------

        print("\nObservation")
        print("-------------------------")
        print(result["observation"])

        # ---------------------------------------
        # Signals
        # ---------------------------------------

        print("\nSignals")
        print("-------------------------")

        for signal in sorted(result["signals"]):
            print(signal)

        # ---------------------------------------
        # Interpretations
        # ---------------------------------------

        print("\nInterpretations")
        print("-------------------------")

        if result["interpretations"]:
            for interpretation in sorted(result["interpretations"]):
                print(interpretation)
        else:
            print("(none)")

        # ---------------------------------------
        # Decision
        # ---------------------------------------

        print("\nDecision")
        print("-------------------------")

        decision = result["decision"]

        print(f"Decision   : {decision['decision']}")
        print(f"Confidence : {decision['confidence']}")

        print("\nReasons")

        if decision["reasons"]:
            for reason in decision["reasons"]:
                print(f"- {reason}")
        else:
            print("(none)")

        # ---------------------------------------
        # Knowledge
        # ---------------------------------------

        print("\nKnowledge")
        print("-------------------------")
        print(
            f"Stored     : "
            f"{result.get('knowledge_saved', False)}"
        )

    print("\n🎉 Scan Cycle Complete")


if __name__ == "__main__":
    main()