# KG-RAG Example

A LangChain + OpenAI + Neo4j GraphRAG example with read-only query validation, budget caps, and structured logging. The offline RDF/SHACL packs run without these services; use them first.

This module currently targets the LangChain 1.x package family.

## What This Example Demonstrates

- Environment-based configuration with no hard-coded secrets
- Read-only Cypher validation before execution
- Structured logging instead of ad-hoc prints
- A testable module layout

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[graphrag]'
cp .env.example .env
```

Fill in these environment variables:

```bash
OPENAI_API_KEY=replace-me
OPENAI_CYPHER_MODEL=gpt-4o-mini
OPENAI_QA_MODEL=gpt-4o-mini
LLM_TIMEOUT_SECONDS=20
MAX_LLM_CALLS=4
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=replace-me
GRAPH_TIMEOUT_SECONDS=20
MAX_GRAPH_QUERIES=2
MAX_QUERY_LENGTH=700
MAX_MATCH_CLAUSES=3
```

## Run

```bash
python3 src/integrations/langchain/kg-rag/graph_rag.py --query "Who manages the team that works on the Alpha Project?"
```

## Security Notes

- Use a Neo4j account with read-only permissions for model-generated queries.
- The example rejects procedures, writes, comments, unbounded paths, Cartesian patterns and other unsafe syntax before execution, but database permissions are still the primary safety control.
- Query complexity and runtime controls are enforced through query-length, MATCH-count, timeout, and per-run call caps.
- Never commit your `.env` file.
