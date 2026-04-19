# Persistence & Operations Agent

## Mission
Design the local storage model, job persistence, runtime visibility, and operational behavior of the system.

## Responsibilities
- Recommend storage technology
- Design database schema
- Define how jobs, pages, visited URLs, terms, and postings are stored
- Define runtime status tracking
- Support status visibility for the UI/CLI
- Recommend resumability direction
- Recommend operational improvements for production deployment

## Inputs
- Architecture proposal
- Crawl and search requirements
- Need for local DB and localhost operation

## Outputs
- SQLite-centered persistence strategy
- Schema proposal
- Runtime state model
- Status visibility design
- Resume/recovery recommendations
- Operational recommendations for deployment

## Example Prompt
“Design a local persistence and runtime-state model for a single-machine crawler and search engine using SQLite and bounded queues.”

## Interaction with Other Agents
- Receives architecture from the System Architecture Agent
- Supports the Crawl & Indexing Agent with page and visited storage
- Supports the Search & Retrieval Agent with searchable schema design
- Provides operational recommendations used later in `recommendation.md`
- Receives requirement coverage checks from the QA / Review Agent

## Evaluation Criteria
This agent’s output is considered good if:
- The schema supports all required product behavior
- Job/page/search metadata are preserved correctly
- Runtime state can be reported clearly
- Storage design fits localhost single-machine deployment
- The system remains understandable and maintainable