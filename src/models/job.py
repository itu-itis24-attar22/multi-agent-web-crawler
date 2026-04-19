from dataclasses import dataclass
from typing import Optional


@dataclass
class Job:
    job_id: Optional[int]
    origin_url: str
    max_depth: int
    status: str
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    pages_discovered: int = 0
    pages_crawled: int = 0
    pages_indexed: int = 0
    pages_failed: int = 0