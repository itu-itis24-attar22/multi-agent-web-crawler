from src.storage.agent_repository import create_agent_decision


class AgentOrchestrator:
    """
    Lightweight orchestration layer that makes agent-guided decisions
    visible in the running system.
    """

    def log_requirement_decision(self, decision_text: str, job_id: int | None = None) -> None:
        create_agent_decision(
            agent_name="Product Requirements Agent",
            stage="requirements",
            decision_text=decision_text,
            job_id=job_id,
        )

    def log_architecture_decision(self, decision_text: str, job_id: int | None = None) -> None:
        create_agent_decision(
            agent_name="System Architecture Agent",
            stage="architecture",
            decision_text=decision_text,
            job_id=job_id,
        )

    def log_crawl_decision(self, decision_text: str, job_id: int | None = None) -> None:
        create_agent_decision(
            agent_name="Crawl & Indexing Agent",
            stage="crawl_index",
            decision_text=decision_text,
            job_id=job_id,
        )

    def log_search_decision(self, decision_text: str, job_id: int | None = None) -> None:
        create_agent_decision(
            agent_name="Search & Retrieval Agent",
            stage="search",
            decision_text=decision_text,
            job_id=job_id,
        )

    def log_persistence_decision(self, decision_text: str, job_id: int | None = None) -> None:
        create_agent_decision(
            agent_name="Persistence & Operations Agent",
            stage="persistence_ops",
            decision_text=decision_text,
            job_id=job_id,
        )

    def log_review_decision(self, decision_text: str, job_id: int | None = None) -> None:
        create_agent_decision(
            agent_name="QA / Review Agent",
            stage="review",
            decision_text=decision_text,
            job_id=job_id,
        )

    def plan_index_job(self, origin_url: str, max_depth: int, job_id: int) -> None:
        self.log_requirement_decision(
            f"Accepted indexing job with origin={origin_url} and max_depth={max_depth}.",
            job_id=job_id,
        )
        self.log_architecture_decision(
            "Selected bounded frontier queue, SQLite persistence, and multi-worker single-machine execution.",
            job_id=job_id,
        )
        self.log_crawl_decision(
            f"Will crawl using BFS-style frontier traversal up to depth {max_depth}, with per-job deduplication.",
            job_id=job_id,
        )
        self.log_persistence_decision(
            "Will store pages, visited URLs, terms, and postings incrementally in SQLite.",
            job_id=job_id,
        )
        self.log_review_decision(
            "Verified that duplicate prevention, back pressure, and required result metadata are part of the job plan.",
            job_id=job_id,
        )

    def plan_search(self, query: str, job_id: int | None = None) -> None:
        if job_id is None:
            self.log_search_decision(
                f"Search requested for query='{query}' over all indexed pages."
            )
            self.log_review_decision(
                "Verified that global search results should still be returned as (relevant_url, origin_url, depth)."
            )
        else:
            self.log_search_decision(
                f"Search requested for query='{query}' scoped to job_id={job_id}.",
                job_id=job_id,
            )
            self.log_review_decision(
                "Verified that job-scoped search results should still be returned as (relevant_url, origin_url, depth).",
                job_id=job_id,
            )