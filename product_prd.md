# Product Requirements Document (PRD)

## 1. Product Overview

This project is a single-machine web crawler and search engine that supports depth-limited crawling and keyword-based retrieval. The system is intended to run locally, store its state in a local database, and provide both CLI and simple web UI access.

The project must also demonstrate a multi-agent AI development workflow. The runtime system itself is not required to be a full LLM multi-agent runtime, but the project must clearly show agent roles, interactions, and decisions.

---

## 2. Goals

The system must:
- crawl from an origin URL up to depth `k`
- avoid crawling the same page twice within a job
- build a searchable index incrementally
- support query search over indexed pages
- return results as `(relevant_url, origin_url, depth)`
- expose progress and system state
- show bounded-load behavior
- demonstrate multi-agent workflow clearly

---

## 3. Functional Requirements

### 3.1 Indexing
The system must provide:

```text
index(origin, k)

Behavior:

begin from origin
crawl pages up to depth k
treat depth as number of hops from origin
index the page at depth k
do not enqueue children beyond depth k
prevent duplicate crawling per job
3.2 Search

The system must provide:

search(query)

Behavior:

normalize query text
retrieve matching pages from the inverted index
rank results using a reasonable scoring strategy
return triples:
relevant_url
origin_url
depth
3.3 Runtime Visibility

The system must expose:

job list
job details
crawled/indexed counts
queue depth
pressure state
page inspection
3.4 Multi-Agent Visibility

The system must visibly represent agent-guided decisions through:

workflow documentation
per-agent description files
runtime decision logging
4. Non-Functional Requirements
local execution only
single-machine design
mostly language-native implementation
bounded work queue
understandable architecture
modular codebase
maintainable storage model
suitable for grading and demonstration
5. Architecture Requirements

The solution should be organized into these logical components:

crawler
frontier
workers
parser
indexer
search engine
persistence layer
CLI
web UI
agent orchestration layer
6. Data Requirements

The system must persist:

jobs
pages
visited URLs
search terms
postings
agent decisions
7. Interface Requirements
CLI

Must support:

initialization
indexing
job listing
job inspection
search
shell access
agent decision inspection
Web UI

Must support:

start indexing
view jobs
view job details
inspect pages
search
inspect recent and job-specific agent decisions
8. Search While Indexing Requirement

Even though the assignment allows assuming indexing is invoked before search, the design should credibly support search during active indexing.

This project addresses that by:

indexing pages incrementally
storing terms/postings immediately
allowing background indexing while search reads current DB state
9. Back Pressure Requirement

The crawler must include controlled load behavior.

This project addresses that by:

bounded frontier queue
worker-count limits
runtime queue state
pressure event tracking
10. Multi-Agent Workflow Requirement

Defined agents must include specialized responsibilities such as:

requirements
architecture
crawling/indexing
search/retrieval
persistence/operations
QA/review

The project owner is responsible for:

integrating outputs
resolving tradeoffs
making final decisions
11. Acceptance Criteria

The project is complete when:

indexing works correctly up to depth k
duplicate crawling is prevented within a job
search returns correct triples
the search index is updated incrementally
runtime status is visible
back pressure exists and is visible
CLI works
web UI works
multi-agent workflow is documented
agent decisions are visible in runtime or clearly recorded
12. Deliverables

Required deliverables:

product_prd.md
README.md
recommendation.md
multi_agent_workflow.md
GitHub repository / working codebase

Strongly included:

/agents/*.md
agent_decision_log.md
agent_prompt_pack.md