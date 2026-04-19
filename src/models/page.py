from dataclasses import dataclass
from typing import Optional


@dataclass
class Page:
    page_id: Optional[int]
    job_id: int
    page_url: str
    origin_url: str
    depth: int
    status: str
    http_status: Optional[int] = None
    title: Optional[str] = None
    content_text: Optional[str] = None
    content_hash: Optional[str] = None
    discovered_at: Optional[str] = None
    fetched_at: Optional[str] = None
    indexed_at: Optional[str] = None
    error_message: Optional[str] = None