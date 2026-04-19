# Crawl & Indexing Agent

## Mission
Design the crawling and indexing pipeline for `index(origin, k)`.

## Responsibilities
- Define crawl frontier behavior
- Define BFS-style depth handling
- Define URL normalization rules
- Define duplicate prevention strategy
- Define worker behavior and queue interaction
- Define how extracted text becomes incrementally indexed
- Help design back pressure behavior

## Inputs
- System architecture proposal
- Product requirements
- Max depth and duplicate prevention constraints

## Outputs
- Crawl pipeline design
- Frontier behavior
- URL normalization approach
- Deduplication strategy
- Incremental indexing flow
- Worker loop design

## Example Prompt
“Design the crawling pipeline for a single-machine search engine with bounded queue depth, URL normalization, per-job deduplication, and incremental indexing.”

## Interaction with Other Agents
- Receives architecture from the System Architecture Agent
- Coordinates with the Search & Retrieval Agent on incremental indexing
- Coordinates with the Persistence & Operations Agent on page and visited URL storage
- Receives requirement coverage feedback from the QA / Review Agent

## Evaluation Criteria
This agent’s output is considered good if:
- Depth-limited crawl logic is correct
- Duplicate crawling is prevented
- Queue/back pressure behavior is explicit
- Indexed pages can become searchable incrementally
- The design is implementable with language-native tools