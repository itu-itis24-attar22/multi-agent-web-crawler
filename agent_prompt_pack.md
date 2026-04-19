# Agent Prompt Pack

This document contains example prompts used to guide each AI agent during the project.

---

## Product Requirements Agent

**Prompt**
Read the assignment and convert it into a clear set of functional requirements, non-functional requirements, constraints, assumptions, and acceptance criteria for a single-machine web crawler and search engine built through a multi-agent AI workflow.

---

## System Architecture Agent

**Prompt**
Design a single-machine architecture for a crawler and search engine that supports `index(origin, k)` and `search(query)`, prevents duplicate crawling within a job, uses bounded-load back pressure, supports incremental indexing, and provides CLI/UI visibility.

---

## Crawl & Indexing Agent

**Prompt**
Design the crawling and indexing pipeline, including frontier behavior, URL normalization, per-job deduplication, BFS-style traversal, worker behavior, and page-by-page indexing.

---

## Search & Retrieval Agent

**Prompt**
Design the search subsystem using an inverted index. Search must return results as `(relevant_url, origin_url, depth)`, support reasonable ranking, and optionally support job-scoped search.

---

## Persistence & Operations Agent

**Prompt**
Design the SQLite schema and runtime state model for a single-machine crawler. Include jobs, pages, visited URLs, terms, postings, and agent decisions. Also recommend how queue state and pressure should be exposed.

---

## QA / Review Agent

**Prompt**
Review the proposed crawler and search system against the assignment requirements. Identify missing features, weak assumptions, scalability problems, workflow evidence gaps, or anything that may make the project look too similar to Project 1.

---

## Runtime Agent Layer Prompt Idea

**Prompt**
Record structured runtime planning decisions for indexing and search so that the multi-agent process is visible in the running application without requiring a live LLM runtime.