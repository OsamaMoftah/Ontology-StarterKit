# 30-Day Ontology Sprint

A 30-day plan for your first ontology-backed AI feature. Adjust the timing to your team.

## Phase 1: Define the Problem (Days 1-5)

- Pick the one business problem this ontology solves. Do not scope two.
- Draft 5 to 10 competency questions.
- Fill out the [ROI template](../for-product-managers/roi-calculator/roi-template.md).
- Use the [decision framework](../for-product-managers/decision-framework.md) to choose the data model.
- Sketch a minimal schema. Start with 5–10 classes.

## Phase 2: Ingest and Shape Data (Days 6-15)

- Provision a graph store.
- Load a representative slice of data.
- Extract entities and relations from unstructured text if needed.
- Review whether the ontology answers the competency questions.

## Phase 3: Integrate With the AI Layer (Days 16-25)

- Implement the retrieval layer using the [KG-RAG example](../../src/integrations/langchain/kg-rag/graph_rag.py).
- Test prompts against known-answer questions. Validate LLM outputs before they reach users.
- Add hybrid retrieval only if exact graph traversal is not enough.
- Run an internal alpha with real product questions.

## Phase 4: Prepare for Production (Days 26-30)

- Add validation and tests.
- Set up the [schema-change review process](../governance/schema-change-review.md).
- Add caching or cost controls where needed.
- Document the MVP ontology and launch criteria.
- After launch, track the ROI template's numbers: hallucination rate, rework hours, and query latency.
