import sqlite3
from collections import Counter
from typing import Optional

from src.storage.database import get_connection


def get_term_id(term_text: str) -> Optional[int]:
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT term_id
            FROM terms
            WHERE term_text = ?
            """,
            (term_text,),
        ).fetchone()

    return row["term_id"] if row else None


def create_term(term_text: str) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO terms (term_text)
            VALUES (?)
            """,
            (term_text,),
        )
        conn.commit()
        return cursor.lastrowid


def get_or_create_term(term_text: str) -> int:
    term_id = get_term_id(term_text)
    if term_id is not None:
        return term_id

    try:
        return create_term(term_text)
    except sqlite3.IntegrityError:
        existing_term_id = get_term_id(term_text)
        if existing_term_id is not None:
            return existing_term_id
        raise


def upsert_posting(term_id: int, page_id: int, term_frequency: int) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO postings (term_id, page_id, term_frequency)
            VALUES (?, ?, ?)
            ON CONFLICT(term_id, page_id)
            DO UPDATE SET term_frequency = excluded.term_frequency
            """,
            (term_id, page_id, term_frequency),
        )
        conn.commit()


def index_page_terms(page_id: int, tokens: list[str]) -> None:
    token_counts = Counter(tokens)

    for term_text, frequency in token_counts.items():
        term_id = get_or_create_term(term_text)
        upsert_posting(term_id, page_id, frequency)

def search_pages_by_terms(
    query_terms: list[str],
    limit: int = 20,
    job_id: int | None = None,
) -> list[dict]:
    """
    Efficient search:
    - joins terms, postings, pages
    - computes score in SQL
    - deduplicates final output by (page_url, origin_url, depth)
    - optionally filters by job_id
    """
    if not query_terms:
        return []

    placeholders = ",".join("?" for _ in query_terms)
    params: list = list(query_terms)

    job_filter_sql = ""
    if job_id is not None:
        job_filter_sql = " AND pg.job_id = ? "
        params.append(job_id)

    params.append(limit)

    with get_connection() as conn:
        rows = conn.execute(
            f"""
            SELECT
                page_url,
                origin_url,
                depth,
                MAX(score) AS score
            FROM (
                SELECT
                    pg.page_id,
                    pg.page_url,
                    pg.origin_url,
                    pg.depth,
                    SUM(po.term_frequency) AS score
                FROM terms t
                JOIN postings po ON t.term_id = po.term_id
                JOIN pages pg ON po.page_id = pg.page_id
                WHERE t.term_text IN ({placeholders})
                  AND pg.status = 'indexed'
                  {job_filter_sql}
                GROUP BY pg.page_id, pg.page_url, pg.origin_url, pg.depth
            ) AS page_scores
            GROUP BY page_url, origin_url, depth
            ORDER BY score DESC, depth ASC, page_url ASC
            LIMIT ?
            """,
            tuple(params),
        ).fetchall()

    return [dict(row) for row in rows]