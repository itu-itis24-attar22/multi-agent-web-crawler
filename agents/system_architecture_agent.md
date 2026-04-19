# System Architecture Agent

## Mission
Design the overall system architecture for the crawler, indexer, search engine, storage layer, and interface.

## Responsibilities
- Propose a clean single-machine architecture
- Separate responsibilities between crawler, indexer, search, storage, and UI/CLI
- Define data flow through the system
- Define how search can work while indexing is active
- Recommend concurrency and back pressure strategy
- Recommend storage model

## Inputs
- Requirements and acceptance criteria from the Product Requirements Agent
- Assignment constraints
- Single-machine scalability expectation

## Outputs
- Architecture proposal
- Component responsibilities
- Data flow description
- Concurrency strategy
- Storage recommendation
- UI/CLI direction

## Example Prompt
“Design a single-machine architecture for a crawler and search engine that supports depth-limited indexing, duplicate prevention, bounded load, and search over incrementally indexed pages.”

## Interaction with Other Agents
- Receives requirements from the Product Requirements Agent
- Provides architecture direction to the Crawl & Indexing Agent
- Provides architecture direction to the Search & Retrieval Agent
- Provides architecture constraints to the Persistence & Operations Agent
- Receives review feedback from the QA / Review Agent

## Evaluation Criteria
This agent’s output is considered good if:
- The architecture clearly separates concerns
- The design supports the required features
- Back pressure is addressed explicitly
- Search during active indexing is explained credibly
- The design is suitable for a single machine