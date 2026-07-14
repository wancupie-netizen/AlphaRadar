import uuid
from datetime import datetime

from scanner.database import supabase


def start_job(token):

    return {
        "job_id": str(uuid.uuid4()),
        "token": token,
        "started_at": datetime.utcnow()
    }


def finish_job(job, status, error=None):

    finished_at = datetime.utcnow()

    duration = int(
        (finished_at - job["started_at"]).total_seconds() * 1000
    )

    supabase.table("pulse_logs").insert({

        "job_id": job["job_id"],
        "token": job["token"],
        "status": status,
        "started_at": job["started_at"].isoformat(),
        "finished_at": finished_at.isoformat(),
        "duration_ms": duration,
        "error": error

    }).execute()

    return duration