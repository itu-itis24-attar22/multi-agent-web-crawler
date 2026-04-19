import threading


class StateTracker:
    def __init__(self, frontier_maxsize: int) -> None:
        self._lock = threading.Lock()

        self.frontier_maxsize = frontier_maxsize
        self.frontier_size = 0
        self.active_workers = 0
        self.total_enqueued = 0
        self.total_dequeued = 0
        self.back_pressure_events = 0

    def set_frontier_size(self, size: int) -> None:
        with self._lock:
            self.frontier_size = size

    def increment_enqueued(self, amount: int = 1) -> None:
        with self._lock:
            self.total_enqueued += amount

    def increment_dequeued(self, amount: int = 1) -> None:
        with self._lock:
            self.total_dequeued += amount

    def increment_back_pressure_events(self, amount: int = 1) -> None:
        with self._lock:
            self.back_pressure_events += amount

    def worker_started(self) -> None:
        with self._lock:
            self.active_workers += 1

    def worker_finished(self) -> None:
        with self._lock:
            self.active_workers -= 1

    def snapshot(self) -> dict:
        with self._lock:
            pressure_ratio = (
                self.frontier_size / self.frontier_maxsize
                if self.frontier_maxsize > 0
                else 0.0
            )

            if pressure_ratio >= 1.0:
                pressure_state = "FULL"
            elif pressure_ratio >= 0.8:
                pressure_state = "HIGH"
            elif pressure_ratio >= 0.5:
                pressure_state = "MEDIUM"
            else:
                pressure_state = "LOW"

            return {
                "frontier_size": self.frontier_size,
                "frontier_maxsize": self.frontier_maxsize,
                "active_workers": self.active_workers,
                "total_enqueued": self.total_enqueued,
                "total_dequeued": self.total_dequeued,
                "back_pressure_events": self.back_pressure_events,
                "pressure_state": pressure_state,
            }