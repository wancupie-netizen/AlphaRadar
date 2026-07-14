from scanner.dexscreener import search_token
from scanner.pair_selector import select_best_pair
from scanner.normalizer import normalize_pair
from scanner.database import save_market_event

from scanner.observation_builder import build_observation
from scanner.intelligence_engine import build_intelligence

from scanner.knowledge_gate import should_store
from scanner.intelligence_store import (
    load_latest_intelligence,
    save_intelligence,
)

from pulse.pulse import start_job, finish_job


def run_scan(token):
    """
    Run a complete AlphaRadar Scan Job.

    Pipeline

        Start Pulse
            ↓
        Scan DexScreener
            ↓
        Select Best Pair
            ↓
        Normalize Market Data
            ↓
        Save Market Event
            ↓
        Build Observation
            ↓
        Build Intelligence
            ↓
        Knowledge Persistence
            ↓
        Finish Pulse
            ↓
        Return Result
    """

    job = start_job(token)

    try:

        # ---------------------------------------
        # Step 1 : Scan DexScreener
        # ---------------------------------------

        data = search_token(token)

        # ---------------------------------------
        # Step 2 : Select Best Pair
        # ---------------------------------------

        pairs = data.get("pairs", [])

        selected_pair = select_best_pair(pairs)

        if selected_pair is None:

            finish_job(
                job,
                "FAILED",
                "No valid pair found",
            )

            return {
                "success": False,
                "job_status": "FAILED",
                "token": token,
                "error": "No valid pair found",
            }

        # ---------------------------------------
        # Step 3 : Normalize
        # ---------------------------------------

        event = normalize_pair(selected_pair)

        # ---------------------------------------
        # Step 4 : Save Market Event
        # ---------------------------------------

        save_market_event(event)

        # ---------------------------------------
        # Step 5 : Observation
        # ---------------------------------------

        observation = build_observation(token)

        if observation is None:

            duration = finish_job(
                job,
                "SUCCESS",
            )

            return {
                "success": True,
                "job_status": "SUCCESS",
                "token": token,
                "duration_ms": duration,
                "event": event,
                "message": (
                    "First market event recorded. "
                    "Waiting for next scan."
                ),
            }

        # ---------------------------------------
        # Step 6 : Intelligence Engine
        # ---------------------------------------

        intelligence_package = build_intelligence(
            token,
            observation,
        )

        # ---------------------------------------
        # Step 7 : Knowledge Gate
        # ---------------------------------------

        latest_package = load_latest_intelligence(
            token,
        )

        knowledge_saved = False

        if should_store(
            intelligence_package,
            latest_package,
        ):

            save_intelligence(
                intelligence_package,
            )

            knowledge_saved = True

        # ---------------------------------------
        # Step 8 : Finish
        # ---------------------------------------

        duration = finish_job(
            job,
            "SUCCESS",
        )

        # ---------------------------------------
        # Step 9 : Return
        # ---------------------------------------

        return {

            "success": True,

            "job_status": "SUCCESS",

            "token": token,

            "duration_ms": duration,

            "event": event,

            "intelligence_package": intelligence_package,

            "knowledge_saved": knowledge_saved,

            # Backward compatibility

            "observation":
                intelligence_package["observation"],

            "signals":
                intelligence_package["signals"],

            "interpretations":
                intelligence_package["interpretations"],

            "decision":
                intelligence_package["decision"],

        }

    except Exception as e:

        print("\n❌ AlphaRadar Exception")
        print(type(e).__name__)
        print(e)

        try:

            finish_job(
                job,
                "FAILED",
                str(e),
            )

        except Exception as pulse_error:

            print("\n⚠️ Pulse Update Failed")
            print(type(pulse_error).__name__)
            print(pulse_error)

        return {

            "success": False,

            "job_status": "FAILED",

            "token": token,

            "error": str(e),

        }