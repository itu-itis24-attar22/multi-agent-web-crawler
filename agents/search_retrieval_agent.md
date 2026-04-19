# Search & Retrieval Agent

## Mission
Design the search subsystem for `search(query)` and define how relevant results are returned.

## Responsibilities
- Define query normalization and tokenization approach
- Define inverted index structure
- Define relevance scoring strategy
- Define result format `(relevant_url, origin_url, depth)`
- Ensure search works against incrementally written indexed data
- Suggest efficient query execution

## Inputs
- Product requirements
- Architecture proposal
- Crawl/indexing pipeline assumptions
- Storage design

## Outputs
- Search flow design
- Query normalization strategy
- Inverted index usage plan
- Ranking strategy
- Result formatting rules
- SQL/data-access suggestions

## Example Prompt
“Design an efficient query path for a single-machine crawler search engine using an inverted index and returning `(relevant_url, origin_url, depth)`.”

## Interaction with Other Agents
- Receives architecture from the System Architecture Agent
- Coordinates with the Crawl & Indexing Agent on incremental indexing
- Coordinates with the Persistence & Operations Agent on terms/postings/pages schema
- Receives correctness and edge-case feedback from the QA / Review Agent

## Evaluation Criteria
This agent’s output is considered good if:
- Search returns the required triple format
- Relevance logic is simple, reasonable, and explainable
- Search can operate on incrementally indexed pages
- Query execution is efficient for the scale expected in the project