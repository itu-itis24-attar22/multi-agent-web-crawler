from dataclasses import dataclass


@dataclass
class CrawlItem:
    job_id: int
    url: str
    origin_url: str
    depth: int