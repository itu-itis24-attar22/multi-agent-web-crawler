from datetime import datetime
from typing import Optional

from src.storage.database import get_connection


def utc_now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds")


def create_job(origin_url: str, max_depth: int, status: str = "queued") -> int:
    created_at = utc_now_iso()

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO jobs (
                origin_url,
                max_depth,
                status,
                created_at
            )
            VALUES (?, ?, ?, ?)
            """,
            (origin_url, max_depth, status, created_at),
        )
        conn.commit()
        return cursor.lastrowid


def get_job(job_id: int) -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM jobs WHERE job_id = ?",
            (job_id,),
        ).fetchone()

    return dict(row) if row else None


def list_jobs() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM jobs ORDER BY job_id DESC"
        ).fetchall()

    return [dict(row) for row in rows]


def update_job_status(job_id: int, status: str) -> None:
    started_at = utc_now_iso() if status == "running" else None
    completed_at = utc_now_iso() if status in {"completed", "failed", "stopped"} else None

    with get_connection() as conn:
        if started_at:
            conn.execute(
                """
                UPDATE jobs
                SET status = ?, started_at = ?
                WHERE job_id = ?
                """,
                (status, started_at, job_id),
            )
        elif completed_at:
            conn.execute(
                """
                UPDATE jobs
                SET status = ?, completed_at = ?
                WHERE job_id = ?
                """,
                (status, completed_at, job_id),
            )
        else:
            conn.execute(
                """
                UPDATE jobs
                SET status = ?
                WHERE job_id = ?
                """,
                (status, job_id),
            )

        conn.commit()


def increment_job_counter(job_id: int, field_name: str, amount: int = 1) -> None:
    allowed_fields = {
        "pages_discovered",
        "pages_crawled",
        "pages_indexed",
        "pages_failed",
    }

    if field_name not in allowed_fields:
        raise ValueError(f"Invalid counter field: {field_name}")

    with get_connection() as conn:
        conn.execute(
            f"""
            UPDATE jobs
            SET {field_name} = {field_name} + ?
            WHERE job_id = ?
            """,
            (amount, job_id),
        )
        conn.commit()