from datetime import datetime
from src.storage.database import get_connection


def utc_now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds")


def create_agent_decision(
    agent_name: str,
    stage: str,
    decision_text: str,
    job_id: int | None = None,
) -> int:
    created_at = utc_now_iso()

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO agent_decisions (
                job_id,
                agent_name,
                stage,
                decision_text,
                created_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (job_id, agent_name, stage, decision_text, created_at),
        )
        conn.commit()
        return cursor.lastrowid


def list_agent_decisions(job_id: int | None = None) -> list[dict]:
    with get_connection() as conn:
        if job_id is None:
            rows = conn.execute(
                """
                SELECT *
                FROM agent_decisions
                ORDER BY decision_id DESC
                """
            ).fetchall()
        else:
            rows = conn.execute(
                """
                SELECT *
                FROM agent_decisions
                WHERE job_id = ?
                ORDER BY decision_id ASC
                """,
                (job_id,),
            ).fetchall()

    return [dict(row) for row in rows]