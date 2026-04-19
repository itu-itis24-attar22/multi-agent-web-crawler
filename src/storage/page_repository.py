import sqlite3
from datetime import datetime
from typing import Optional

from src.storage.database import get_connection


def utc_now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds")


def add_visited_url(job_id: int, normalized_url: str, first_seen_depth: int) -> bool:
    """
    Returns True if the URL was newly inserted.
    Returns False if it already existed for this job.
    """
    seen_at = utc_now_iso()

    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO visited_urls (
                    job_id,
                    normalized_url,
                    first_seen_depth,
                    seen_at
                )
                VALUES (?, ?, ?, ?)
                """,
                (job_id, normalized_url, first_seen_depth, seen_at),
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def has_visited_url(job_id: int, normalized_url: str) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT 1
            FROM visited_urls
            WHERE job_id = ? AND normalized_url = ?
            """,
            (job_id, normalized_url),
        ).fetchone()

    return row is not None


def create_page(
    job_id: int,
    page_url: str,
    origin_url: str,
    depth: int,
    status: str = "discovered",
) -> int:
    discovered_at = utc_now_iso()

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO pages (
                job_id,
                page_url,
                origin_url,
                depth,
                status,
                discovered_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (job_id, page_url, origin_url, depth, status, discovered_at),
        )
        conn.commit()
        return cursor.lastrowid


def get_page_by_url(job_id: int, page_url: str) -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM pages
            WHERE job_id = ? AND page_url = ?
            """,
            (job_id, page_url),
        ).fetchone()

    return dict(row) if row else None


def get_page_by_id(page_id: int) -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT *
            FROM pages
            WHERE page_id = ?
            """,
            (page_id,),
        ).fetchone()

    return dict(row) if row else None


def mark_page_fetched(
    page_id: int,
    http_status: Optional[int],
    title: Optional[str],
    content_text: Optional[str],
) -> None:
    fetched_at = utc_now_iso()

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE pages
            SET status = 'fetched',
                http_status = ?,
                title = ?,
                content_text = ?,
                fetched_at = ?
            WHERE page_id = ?
            """,
            (http_status, title, content_text, fetched_at, page_id),
        )
        conn.commit()


def mark_page_indexed(page_id: int) -> None:
    indexed_at = utc_now_iso()

    with get_connection() as conn:
        conn.execute(
            """
            UPDATE pages
            SET status = 'indexed',
                indexed_at = ?
            WHERE page_id = ?
            """,
            (indexed_at, page_id),
        )
        conn.commit()


def mark_page_failed(
    page_id: int,
    error_message: str,
    http_status: Optional[int] = None,
) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE pages
            SET status = 'failed',
                error_message = ?,
                http_status = ?
            WHERE page_id = ?
            """,
            (error_message, http_status, page_id),
        )
        conn.commit()


def list_pages_for_job(job_id: int) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM pages
            WHERE job_id = ?
            ORDER BY depth ASC, page_id ASC
            """,
            (job_id,),
        ).fetchall()

    return [dict(row) for row in rows]