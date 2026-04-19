import threading
from queue import Empty
from src.core.config import (
    DEFAULT_FRONTIER_GET_TIMEOUT_SECONDS,
    DEFAULT_FRONTIER_MAXSIZE,
    DEFAULT_MAX_WORKERS,
)
from src.core.state_tracker import StateTracker
from src.crawler.frontier import Frontier
from src.crawler.normalizer import normalize_url
from src.crawler.worker import process_crawl_item
from src.models.crawl_item import CrawlItem
from src.storage.job_repository import (
    create_job,
    get_job,
    increment_job_counter,
    update_job_status,
)
from src.storage.page_repository import add_visited_url


def _worker_loop(
    frontier: Frontier,
    tracker: StateTracker,
    max_depth: int,
    stop_event: threading.Event,
) -> None:
    tracker.worker_started()

    try:
        while not stop_event.is_set():
            try:
                item = frontier.get(
                    block=True,
                    timeout=DEFAULT_FRONTIER_GET_TIMEOUT_SECONDS,
                )
            except Empty:
                if frontier.empty():
                    break
                continue

            tracker.increment_dequeued(1)
            tracker.set_frontier_size(frontier.qsize())

            try:
                process_crawl_item(
                    frontier=frontier,
                    item=item,
                    max_depth=max_depth,
                    tracker=tracker,
                )
            finally:
                frontier.task_done()
                tracker.set_frontier_size(frontier.qsize())
    finally:
        tracker.worker_finished()


def prepare_indexing_job(origin_url: str, max_depth: int) -> tuple[int, str]:
    normalized_origin = normalize_url(origin_url, origin_url)
    if not normalized_origin:
        raise ValueError(f"Invalid origin URL: {origin_url}")

    job_id = create_job(
        origin_url=normalized_origin,
        max_depth=max_depth,
        status="queued",
    )
    return job_id, normalized_origin


def execute_indexing_job(
    job_id: int,
    normalized_origin: str,
    max_depth: int,
    worker_count: int = DEFAULT_MAX_WORKERS,
    tracker: StateTracker | None = None,
) -> dict:
    tracker = tracker or StateTracker(frontier_maxsize=DEFAULT_FRONTIER_MAXSIZE)

    try:
        update_job_status(job_id, "running")

        frontier = Frontier(maxsize=DEFAULT_FRONTIER_MAXSIZE)

        origin_added = add_visited_url(
            job_id=job_id,
            normalized_url=normalized_origin,
            first_seen_depth=0,
        )
        if not origin_added:
            raise RuntimeError("Failed to register origin URL as visited.")

        pushed = frontier.put(
            CrawlItem(
                job_id=job_id,
                url=normalized_origin,
                origin_url=normalized_origin,
                depth=0,
            ),
            block=False,
        )
        if not pushed:
            tracker.increment_back_pressure_events()
            raise RuntimeError("Failed to enqueue origin URL: frontier is full.")

        increment_job_counter(job_id, "pages_discovered", 1)
        tracker.increment_enqueued(1)
        tracker.set_frontier_size(frontier.qsize())

        stop_event = threading.Event()
        threads: list[threading.Thread] = []

        actual_worker_count = max(1, worker_count)

        for i in range(actual_worker_count):
            thread = threading.Thread(
                target=_worker_loop,
                args=(frontier, tracker, max_depth, stop_event),
                name=f"crawler-worker-{i+1}",
                daemon=True,
            )
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        update_job_status(job_id, "completed")
        return tracker.snapshot()

    except Exception:
        update_job_status(job_id, "failed")
        raise


def run_indexing_job(
    origin_url: str,
    max_depth: int,
    worker_count: int = DEFAULT_MAX_WORKERS,
) -> tuple[int, dict]:
    job_id, normalized_origin = prepare_indexing_job(origin_url, max_depth)

    runtime_status = execute_indexing_job(
        job_id=job_id,
        normalized_origin=normalized_origin,
        max_depth=max_depth,
        worker_count=worker_count,
    )
    return job_id, runtime_status


def get_indexing_job_summary(job_id: int) -> dict | None:
    return get_job(job_id)