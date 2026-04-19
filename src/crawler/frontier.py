from queue import Queue, Full, Empty
from typing import Optional

from src.models.crawl_item import CrawlItem


class Frontier:
    def __init__(self, maxsize: int) -> None:
        self._queue: Queue[CrawlItem] = Queue(maxsize=maxsize)

    def put(self, item: CrawlItem, block: bool = True, timeout: Optional[float] = None) -> bool:
        try:
            self._queue.put(item, block=block, timeout=timeout)
            return True
        except Full:
            return False

    def get(self, block: bool = True, timeout: Optional[float] = None) -> CrawlItem:
        return self._queue.get(block=block, timeout=timeout)

    def task_done(self) -> None:
        self._queue.task_done()

    def qsize(self) -> int:
        return self._queue.qsize()

    def empty(self) -> bool:
        return self._queue.empty()

    def join(self) -> None:
        self._queue.join()