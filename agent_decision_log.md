# Agent Decision Log

This document records key design decisions made during the project and shows how different AI agents contributed to them.

---

## Decision 1 — Storage Strategy

### Options Considered
- Raw file-based storage
- SQLite local database

### Agent Contributions
- **Persistence & Operations Agent** recommended SQLite for structured storage, local querying, and simplicity on a single machine.
- **System Architecture Agent** agreed that SQLite fits localhost deployment and incremental indexing.
- **QA / Review Agent** noted that raw files would weaken search consistency and inspectability.

### Final Decision
SQLite was selected as the local persistence layer.

---

## Decision 2 — Duplicate Prevention

### Options Considered
- Global deduplication across all jobs
- Per-job deduplication

### Agent Contributions
- **Crawl & Indexing Agent** recommended per-job deduplication because it is simpler and matches crawl job semantics.
- **Search & Retrieval Agent** noted that per-job tracking preserves `origin_url` and `depth` relationships cleanly.
- **QA / Review Agent** confirmed that the assignment only requires preventing duplicate crawling within a job.

### Final Decision
Per-job deduplication was implemented using `visited_urls`.

---

## Decision 3 — Indexing Strategy

### Options Considered
- Index after crawl completion
- Incremental page-by-page indexing

### Agent Contributions
- **Search & Retrieval Agent** recommended incremental indexing so search can reflect newly indexed pages.
- **Crawl & Indexing Agent** confirmed that indexing can happen immediately after parsing each page.
- **System Architecture Agent** supported this because it improves the “search while indexing” story.

### Final Decision
Incremental indexing was implemented.

---

## Decision 4 — Back Pressure

### Options Considered
- Unbounded crawl queue
- Bounded frontier queue

### Agent Contributions
- **System Architecture Agent** recommended a bounded queue to control load.
- **Persistence & Operations Agent** suggested exposing queue size and pressure state to the interface.
- **QA / Review Agent** identified back pressure as a required assignment feature.

### Final Decision
A bounded frontier queue with runtime pressure visibility was implemented.

---

## Decision 5 — Interface Strategy

### Options Considered
- CLI only
- CLI + web UI

### Agent Contributions
- **System Architecture Agent** recommended CLI first for speed and clarity.
- **QA / Review Agent** suggested adding a simple web UI to make grading easier.
- **Persistence & Operations Agent** supported a UI because it improves visibility of jobs and pages.

### Final Decision
Both CLI and a simple web UI were implemented.

---

## Decision 6 — Search Scope

### Options Considered
- Global search only
- Global and job-scoped search

### Agent Contributions
- **Search & Retrieval Agent** recommended optional job-scoped search for cleaner debugging and clearer agent decision traces.
- **QA / Review Agent** noted that job-scoped search makes result provenance easier to explain.

### Final Decision
Search supports optional job scoping.

---

## Decision 7 — Multi-Agent Visibility

### Options Considered
- Workflow documented only in markdown
- Workflow documented in markdown and reflected in runtime decision traces

### Agent Contributions
- **QA / Review Agent** warned that documentation alone may look too similar to Project 1.
- **System Architecture Agent** proposed a lightweight runtime orchestration layer that records agent decisions without requiring live LLM calls.
- **Persistence & Operations Agent** recommended storing these decisions in SQLite.

### Final Decision
Runtime agent decision logging was added and made visible through CLI. UI visibility is optional depending on presentation preference.

---

## Conclusion

The final system was shaped by multiple specialized agents rather than by a single undifferentiated design process. Their outputs were reviewed, compared, and integrated by the project owner, who made the final implementation decisions.