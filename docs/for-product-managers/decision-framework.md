# Ontology StarterKit Decision Framework

Choosing the right storage and query model is one of the most important design decisions in an ontology-backed AI system.

> **This is this starter kit's opinionated default, not a neutral, benchmarked comparison.** The recommendations below reflect the tradeoffs this repository was built around (fast LLM integration, SHACL-based validation) and are a reasonable starting point, not a substitute for evaluating your own requirements. Where a rating isn't backed by a benchmark we ran ourselves, it links to the vendor's own documentation so you can verify it independently.

## Quick Recommendation

| Primary goal | Recommended path | Why |
| :--- | :--- | :--- |
| GraphRAG for GenAI products | Property graph such as [Neo4j](https://neo4j.com/docs/) | Strong developer tooling and ecosystem support for [LangChain](https://python.langchain.com/docs/integrations/graphs/neo4j_cypher/) and [LlamaIndex](https://docs.llamaindex.ai/en/stable/examples/index_structs/knowledge_graph/Neo4jKGIndexDemo/) integrations |
| Heavy reasoning and strict semantic governance | RDF triplestore such as [GraphDB](https://graphdb.ontotext.com/documentation/) or [RDFox](https://docs.oxfordsemantic.tech/) | Best support for [OWL](https://www.w3.org/TR/owl2-overview/), [SHACL](https://www.w3.org/TR/shacl/), and standards-first validation |
| Search-led product with light graph filtering | Hybrid vector-graph system such as [Weaviate](https://weaviate.io/developers/weaviate) | Supports semantic retrieval with lighter-weight relationship constraints |

## Comparison Matrix

| Feature | Property Graph | RDF Triplestore | Hybrid Vector-Graph |
| :--- | :--- | :--- | :--- |
| Query language | [Cypher](https://neo4j.com/docs/cypher-manual/current/) | [SPARQL](https://www.w3.org/TR/sparql11-query/) | Vendor-specific APIs |
| LLM integration maturity | High — mainstream LangChain/LlamaIndex support | Lower — fewer maintained framework integrations | High — many stores ship native LLM/embedding hooks |
| OWL reasoning | Low to moderate (plugin-dependent) | High — native to most triplestores | Low — not a core feature |
| SHACL-native governance | Low | High — SHACL is an RDF-ecosystem standard | Low |
| Learning curve | Moderate | High — SPARQL and OWL/RDF semantics | Low to moderate |
| Best fit | Product teams building GraphRAG quickly | Regulated or standards-heavy environments | Search-first AI products |

These ratings describe general ecosystem tendencies as of each store's own documentation (linked above), not a controlled evaluation. Treat them as a starting hypothesis to validate against your own stack, not a benchmark result.

**Note on this repository's own example:** `src/ontology/` in this starter kit ships a [SHACL](https://www.w3.org/TR/shacl/)-only example (`shapes.ttl` validating `data.ttl`) — it does not demonstrate OWL reasoning. The "OWL reasoning" row above is a general property of the RDF ecosystem, not something this repo currently exercises; if OWL reasoning is a requirement for you, evaluate it directly against GraphDB or RDFox rather than assuming this repo's example generalizes to it.

## Practical Rule of Thumb

- Start with a property graph if your immediate goal is an LLM-facing product feature.
- Choose RDF first if your main constraint is semantic rigor, validation, or standards compliance.
- Use a hybrid vector-graph store when semantic search is dominant and graph structure is secondary.

## Other Options Worth Evaluating

This framework deliberately narrows to three categories to keep the decision tractable for a fast-moving product team. Depending on your constraints, also consider:

- [Amazon Neptune](https://docs.aws.amazon.com/neptune/) — managed property graph *and* RDF triplestore in one service; worth a look if you're already committed to AWS.
- [Stardog](https://docs.stardog.com/) — RDF triplestore with a built-in reasoning and virtual-graph layer, positioned for enterprise data-integration use cases.
- [TigerGraph](https://docs.tigergraph.com/) — property graph optimized for large-scale analytical graph queries rather than LLM-orchestration ecosystem support.

## Recommended Startup Path

This is this starter kit's specific, opinionated default — not the only valid path. It optimizes for shipping an LLM-facing feature quickly:

1. Start with Neo4j and a minimal domain ontology.
2. Add LangChain or LlamaIndex as the orchestration layer.
3. Add vector retrieval only when graph traversal alone is insufficient.
4. Introduce stronger validation and governance as the ontology matures.
