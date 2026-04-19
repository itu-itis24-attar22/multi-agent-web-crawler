# Agent Decision Log

This document records how different AI agents contributed to key design decisions during the development of the system. It provides concrete evidence of multi-agent collaboration and decision-making.

---

## Decision 1 — Storage Strategy

### Options Proposed
- Product Requirements Agent: simple storage sufficient for assignment
- Persistence & Operations Agent: SQLite database
- Alternative considered: file-based index storage

### Discussion
- File-based storage is simple but weak for search queries
- SQLite provides structured querying, indexing, and consistency
- SQLite aligns with "single-machine" requirement

### Final Decision
SQLite was selected as the storage layer.

---

## Decision 2 — Deduplication Strategy

### Options Proposed
- Crawl & Indexing Agent: per-job deduplication
- Alternative: global deduplication across all jobs

### Discussion
- Global deduplication increases complexity significantly
- Assignment only requires avoiding duplicate crawling within a job
- Per-job deduplication simplifies implementation and aligns with `(origin_url, depth)` semantics

### Final Decision
Per-job deduplication was implemented using `visited_urls`.

---

## Decision 3 — Indexing Strategy

### Options Proposed
- Search & Retrieval Agent: incremental indexing (page-by-page)
- Alternative: index after full crawl

### Discussion
- Incremental indexing enables search while indexing is active
- Delayed indexing simplifies logic but weakens system behavior
- Assignment explicitly hints at active indexing/search interaction

### Final Decision
Incremental indexing was implemented.

---

## Decision 4 — Back Pressure Design

### Options Proposed
- System Architecture Agent: bounded queue
- Alternative: unbounded queue

### Discussion
- Unbounded queue risks memory overflow
- Bounded queue enforces controlled load
- Back pressure visibility improves system observability

### Final Decision
A bounded frontier queue with runtime pressure tracking was implemented.

---

## Decision 5 — Interface Strategy

### Options Proposed
- System Architecture Agent: CLI-only
- QA / Review Agent: add UI for better demonstration

### Discussion
- CLI is sufficient but less intuitive for grading
- UI improves usability and visibility of system state

### Final Decision
Both CLI and a simple web UI were implemented.

---

## Decision 6 — Search While Indexing

### Options Proposed
- System Architecture Agent: background worker threads
- Alternative: strictly sequential execution

### Discussion
- Sequential execution prevents concurrent search
- Background threads allow indexing to continue while UI remains responsive
- Database supports incremental reads

### Final Decision
Background indexing with concurrent search capability was implemented.

---

## Decision 7 — Multi-Agent Workflow Representation

### Options Proposed
- QA Agent: include explicit workflow documentation
- Alternative: implicit workflow only

### Discussion
- Without documentation, multi-agent work is not visible
- Assignment explicitly requires demonstrating agent collaboration

### Final Decision
- `multi_agent_workflow.md`
- `/agents/*.md`
- `agent_decision_log.md`

were created to make the workflow explicit.

---

## Conclusion

This project was not built by a single monolithic design process. Instead, it was shaped by multiple specialized AI agents whose outputs were evaluated and integrated.

The final system reflects selected decisions based on tradeoffs, constraints, and assignment requirements.