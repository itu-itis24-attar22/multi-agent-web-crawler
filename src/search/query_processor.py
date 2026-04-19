from src.models.search_result import SearchResult
from src.storage.term_repository import search_pages_by_terms
from src.utils.text import normalize_text_to_tokens


def search_query(
    query: str,
    limit: int = 20,
    job_id: int | None = None,
) -> list[SearchResult]:
    """
    Execute a search query and return ranked results.
    Optionally scope search to a specific job.
    """
    tokens = normalize_text_to_tokens(query)

    if not tokens:
        return []

    rows = search_pages_by_terms(tokens, limit=limit, job_id=job_id)

    results: list[SearchResult] = [
        SearchResult(
            relevant_url=row["page_url"],
            origin_url=row["origin_url"],
            depth=row["depth"],
            score=float(row["score"]),
        )
        for row in rows
    ]

    return results