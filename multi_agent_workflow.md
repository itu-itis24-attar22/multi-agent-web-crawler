# Multi-Agent Workflow

## Overview

This project was developed using a multi-agent AI workflow. The runtime crawler and search system is not implemented as a full LLM-driven multi-agent platform; instead, specialized agents were defined and used to shape the requirements, architecture, subsystem design, persistence strategy, and review process. The final system also includes a lightweight runtime agent orchestration layer that records agent decisions for indexing and search.

This approach follows the assignment requirement that the final system does not need to be a multi-agent runtime, while still making the multi-agent process visible and inspectable.

---

## Agent Set

The following agents were defined:

1. Product Requirements Agent
2. System Architecture Agent
3. Crawl & Indexing Agent
4. Search & Retrieval Agent
5. Persistence & Operations Agent
6. QA / Review Agent

The project owner acted as the final decision-maker and integrator.

---

## Agent Responsibilities

### Product Requirements Agent
- extract functional and non-functional requirements
- define acceptance criteria
- define scope and constraints

### System Architecture Agent
- propose architecture
- define components and data flow
- recommend concurrency and queue strategy

### Crawl & Indexing Agent
- design crawling behavior
- define URL normalization and deduplication
- define indexing flow

### Search & Retrieval Agent
- design query flow
- define ranking strategy
- ensure output format matches assignment

### Persistence & Operations Agent
- define SQLite schema
- support runtime state visibility
- guide operational decisions

### QA / Review Agent
- check requirement coverage
- identify weaknesses and risks
- validate compliance with the assignment

---

## Workflow Stages

### Stage 1 — Requirements
The Product Requirements Agent converted the assignment into concrete requirements, constraints, and acceptance criteria.

### Stage 2 — Architecture
The System Architecture Agent proposed the overall architecture, including crawler, frontier, workers, parser, SQLite storage, and search engine.

### Stage 3 — Subsystem Design
The Crawl & Indexing Agent, Search & Retrieval Agent, and Persistence & Operations Agent designed the major subsystems.

### Stage 4 — Review
The QA / Review Agent checked whether the design satisfied the assignment requirements and highlighted gaps.

### Stage 5 — Implementation and Integration
The project owner selected and integrated the best outputs into the final implementation.

---

## Runtime Agent Role

To make the multi-agent workflow visible inside the working application, the project includes a lightweight runtime agent orchestration layer.

This layer:
- records indexing planning decisions
- records search planning decisions
- records QA/review validation decisions
- stores them in SQLite
- exposes them in CLI and web UI

Examples:
- indexing plan for a job
- architecture/persistence decisions linked to a job
- search plan linked to a job-scoped query
- QA validation of required output format

---

## Major Decisions Influenced by Agents

### SQLite storage
Selected because it fits localhost single-machine deployment and supports structured storage for jobs, pages, terms, postings, and agent decisions.

### Per-job deduplication
Selected because it aligns with crawl-job semantics and keeps origin/depth relationships clear.

### Incremental indexing
Selected so search can operate while indexing is active.

### Bounded queue back pressure
Selected to explicitly satisfy the load-control requirement.

### CLI plus web UI
Selected so the project is both easy to grade and easy to demonstrate.

### Runtime agent visibility
Added so the multi-agent workflow is not only documented but also visible in the running system.

---

## Human Decision-Maker Role

The project owner was responsible for:
- evaluating agent outputs
- resolving tradeoffs
- approving final design choices
- directing implementation
- ensuring the final system remained aligned with the assignment

The final codebase reflects accepted agent proposals rather than automatic unfiltered generation.

---

## Evidence of Multi-Agent Collaboration

The project includes:
- `agents/*.md` files
- `multi_agent_workflow.md`
- `agent_decision_log.md`
- optional `agent_prompt_pack.md`
- runtime agent decision inspection through CLI and UI

---

## Result

The final project combines:
- a working single-machine crawler and search engine
- bounded-load architecture
- incremental indexing
- CLI and web UI
- visible multi-agent AI workflow in both documentation and runtime decision traces