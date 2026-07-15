# 30-Day Ontology Sprint

This is a suggested execution plan, not a documented case study or a guarantee — no team's outcomes are being reported here. It shows one reasonable way a small team could scope a first ontology-backed AI feature into a fixed 30-day timebox, so the effort doesn't expand into an open-ended research project. Treat the day ranges as a starting allocation to adjust against your own team's velocity and the complexity of your domain.

## Phase 1: Define the Problem (Days 1-5)

- Align on the one business problem the ontology will solve.
- Draft 5 to 10 competency questions.
- Fill out the [ROI template](../for-product-managers/roi-calculator/roi-template.md).
- Use the [decision framework](../for-product-managers/decision-framework.md) to choose the data model.
- Sketch a minimal schema and keep it intentionally small.

## Phase 2: Ingest and Shape Data (Days 6-15)

- Provision a graph store.
- Load a representative slice of data.
- Extract entities and relations from unstructured text if needed.
- Review whether the ontology answers the competency questions.

## Phase 3: Integrate With the AI Layer (Days 16-25)

- Implement the retrieval layer using the [KG-RAG example](../../src/integrations/langchain/kg-rag/graph_rag.py).
- Refine prompts and add output validation.
- Add hybrid retrieval only if exact graph traversal is not enough.
- Run an internal alpha with real product questions.

## Phase 4: Prepare for Production (Days 26-30)

- Add validation and tests.
- Define schema review and versioning rules.
- Add caching or cost controls where needed.
- Document the MVP ontology and launch criteria.
- Measure the metrics from the ROI model after release.
