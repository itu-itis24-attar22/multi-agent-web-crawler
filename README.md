# Multi-Agent Web Crawler and Search Engine

## Overview

This project implements a single-machine web crawler and keyword-based search engine with both CLI and web UI interfaces. It supports depth-limited crawling, duplicate prevention, incremental indexing, and search over indexed pages.

The project was developed using a multi-agent AI workflow. Different AI agents were assigned responsibilities for requirements, architecture, crawling/indexing, search/retrieval, persistence/operations, and QA/review. The final implementation was produced by evaluating and integrating their outputs.

---

## Core Features

- `index(origin, k)` depth-limited crawling
- Per-job duplicate prevention
- Incremental page indexing
- SQLite-based local storage
- Search returning:
  - `(relevant_url, origin_url, depth)`
- Runtime back pressure visibility
- Multi-worker crawling
- Interactive shell
- Simple web UI
- Runtime-visible agent decisions

---

## Project Structure

```text
.
├── main.py
├── README.md
├── product_prd.md
├── recommendation.md
├── multi_agent_workflow.md
├── agent_decision_log.md
├── agents/
├── src/
├── docs/
├── tests/
└── data/

Technologies Used
Python
SQLite
Flask
Standard library modules:
threading
queue
urllib
html.parser
argparse or equivalent command routing
How the System Works
1. Indexing

The system starts from an origin URL and crawls links up to depth k.

During indexing it:

normalizes URLs
avoids duplicate crawling within the same job
fetches HTML content
extracts text and links
stores page metadata
tokenizes text
updates the inverted index
2. Search

The system:

normalizes the query
finds matching indexed terms
ranks pages using term-frequency-based scoring
returns results as:
relevant URL
origin URL
depth
3. Runtime State

The system tracks:

queue depth
active workers
enqueued/dequeued counts
back pressure events
pressure level
4. Agent Layer

A lightweight agent orchestration layer records:

indexing planning decisions
search planning decisions
QA/review decisions

These decisions are stored and can be viewed in CLI and UI.

Database Schema

Core tables:

jobs
pages
visited_urls
terms
postings
agent_decisions
CLI Usage
Initialize database
python main.py init
Run indexing
python main.py index https://example.com 1
List jobs
python main.py jobs
Show one job
python main.py job 1
Search
python main.py search example

If your current CLI supports scoped search:

python main.py search example --job-id 1
Show agent decisions
python main.py agent-decisions

Job-specific:

python main.py agent-decisions --job-id 1
Interactive shell
python main.py shell
Web UI Usage
Start UI
python main.py ui

Then open:

http://127.0.0.1:5000
UI Features
Start indexing jobs
View jobs
View job details
View pages for a job
Search indexed pages
View recent agent decisions
View job-specific agent decisions
How to Test
CLI test sequence
python main.py init
python main.py index https://example.com 1
python main.py jobs
python main.py job 1
python main.py search example
python main.py agent-decisions --job-id 1
Shell test sequence
python main.py shell

Then:

help
bg-index https://example.com 1
jobs
job-status 1
pages 1
search example
exit
UI test sequence
Run python main.py ui
Open http://127.0.0.1:5000
Start an indexing job
Open the job page
Run a search
Check agent decisions
Back Pressure

The crawler uses a bounded frontier queue. This prevents uncontrolled growth of pending work and provides a simple load-management mechanism suitable for a single-machine system.

Pressure states are exposed as:

LOW
MEDIUM
HIGH
FULL
Search While Indexing

The system supports search while indexing is active because:

pages are indexed incrementally
indexed terms are written immediately
search reads current committed SQLite state
background indexing keeps the interface responsive
Multi-Agent Workflow

This project was developed using a multi-agent AI workflow.

Defined agents:

Product Requirements Agent
System Architecture Agent
Crawl & Indexing Agent
Search & Retrieval Agent
Persistence & Operations Agent
QA / Review Agent

See:

multi_agent_workflow.md
agents/
agent_decision_log.md
Limitations
Single-machine only
Simple term-frequency ranking
No distributed crawling
No production-grade retry system
No global deduplication across jobs
Resume support is limited
Conclusion

This project satisfies the assignment by combining:

a functioning crawler and search engine
bounded-load single-machine design
runtime visibility
a documented and visible multi-agent AI workflow