from urllib.parse import urlparse

from src.models.crawl_item import CrawlItem
from src.crawler.fetcher import fetch_html
from src.crawler.parser import extract_page_data
from src.crawler.normalizer import normalize_url
from src.utils.text import normalize_text_to_tokens


def _same_host(a: str, b: str) -> bool:
    try:
        return urlparse(a).hostname == urlparse(b).hostname
    except ValueError:
        return False
from src.storage.job_repository import increment_job_counter
from src.storage.page_repository import (
    add_visited_url,
    create_page,
    mark_page_failed,
    mark_page_fetched,
    mark_page_indexed,
)
from src.storage.term_repository import index_page_terms


def process_crawl_item(frontier, item: CrawlItem, max_depth: int, tracker=None) -> None:
    """
    Process one crawl item:
    - fetch page
    - parse page
    - store page
    - index terms
    - enqueue child links if depth < max_depth
    """
    page_id = create_page(
        job_id=item.job_id,
        page_url=item.url,
        origin_url=item.origin_url,
        depth=item.depth,
        status="discovered",
    )

    http_status, content_type, html_text = fetch_html(item.url)
    increment_job_counter(item.job_id, "pages_crawled", 1)

    if html_text is None:
        mark_page_failed(
            page_id=page_id,
            error_message=f"Failed to fetch HTML content (content_type={content_type})",
            http_status=http_status,
        )
        increment_job_counter(item.job_id, "pages_failed", 1)
        return

    title, text, raw_links = extract_page_data(html_text)

    mark_page_fetched(
        page_id=page_id,
        http_status=http_status,
        title=title,
        content_text=text,
    )

    tokens = normalize_text_to_tokens(text)
    index_page_terms(page_id=page_id, tokens=tokens)
    mark_page_indexed(page_id=page_id)
    increment_job_counter(item.job_id, "pages_indexed", 1)

    if item.depth >= max_depth:
        return

    child_depth = item.depth + 1

    for raw_link in raw_links:
        normalized = normalize_url(item.url, raw_link)
        if not normalized:
            continue

        # Stay within the same host as the crawl origin.
        if not _same_host(normalized, item.origin_url):
            continue

        was_added = add_visited_url(
            job_id=item.job_id,
            normalized_url=normalized,
            first_seen_depth=child_depth,
        )

        if not was_added:
            continue

        pushed = frontier.put(
            CrawlItem(
                job_id=item.job_id,
                url=normalized,
                origin_url=item.origin_url,
                depth=child_depth,
            ),
            block=False,
        )

        if pushed:
            increment_job_counter(item.job_id, "pages_discovered", 1)
            if tracker is not None:
                tracker.increment_enqueued(1)
                tracker.set_frontier_size(frontier.qsize())
        else:
            if tracker is not None:
                tracker.increment_back_pressure_events(1)
                tracker.set_frontier_size(frontier.qsize())