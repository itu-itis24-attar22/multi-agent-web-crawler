import threading

from src.core.config import DEFAULT_FRONTIER_MAXSIZE, DEFAULT_MAX_WORKERS
from src.core.indexing_service import prepare_indexing_job, execute_indexing_job
from src.core.state_tracker import StateTracker


class BackgroundJobManager:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._threads: dict[int, threading.Thread] = {}
        self._trackers: dict[int, StateTracker] = {}
        self._errors: dict[int, str] = {}

    def start_index_job(
        self,
        origin_url: str,
        max_depth: int,
        worker_count: int = DEFAULT_MAX_WORKERS,
    ) -> int:
        job_id, normalized_origin = prepare_indexing_job(origin_url, max_depth)
        tracker = StateTracker(frontier_maxsize=DEFAULT_FRONTIER_MAXSIZE)

        def target() -> None:
            try:
                execute_indexing_job(
                    job_id=job_id,
                    normalized_origin=normalized_origin,
                    max_depth=max_depth,
                    worker_count=worker_count,
                    tracker=tracker,
                )
            except Exception as e:
                with self._lock:
                    self._errors[job_id] = str(e)

        thread = threading.Thread(target=target, daemon=True)

        with self._lock:
            self._threads[job_id] = thread
            self._trackers[job_id] = tracker

        thread.start()
        return job_id

    def is_running(self, job_id: int) -> bool:
        with self._lock:
            thread = self._threads.get(job_id)
        return thread.is_alive() if thread else False

    def get_runtime_status(self, job_id: int) -> dict | None:
        with self._lock:
            tracker = self._trackers.get(job_id)
        return tracker.snapshot() if tracker else None

    def get_error(self, job_id: int) -> str | None:
        with self._lock:
            return self._errors.get(job_id)


background_job_manager = BackgroundJobManager()