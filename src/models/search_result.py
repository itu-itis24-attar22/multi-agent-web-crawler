from dataclasses import dataclass


@dataclass
class SearchResult:
    relevant_url: str
    origin_url: str
    depth: int
    score: float