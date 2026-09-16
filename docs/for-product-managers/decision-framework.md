# Ontology StarterKit Decision Framework

Your storage and query model affects cost, query speed, LLM integration, and governance. Use this table to choose a starting point.

> These recommendations are opinionated. They optimize for fast LLM integration and SHACL validation. Ratings link to vendor documentation; test them against your own stack.

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

**Note on this repository's own example:** `src/ontology/` in this starter kit ships a [SHACL](https://www.w3.org/TR/shacl/)-only example (`shapes.ttl` validating `data.ttl`) — it does not demonstrate OWL reasoning. The "OWL reasoning" row above is a general property of the RDF ecosystem, not something this repo currently exercises; if OWL reasoning is a requirement for you, evaluate it directly against GraphDB or RDFox rather than assuming this repo's example generalizes to it.

## Rule of Thumb

- Start with a property graph if your immediate goal is an LLM-facing product feature.
- Choose RDF first if your main constraint is semantic rigor, validation, or standards compliance.
- Use a hybrid vector-graph store when semantic search is dominant and graph structure is secondary.

## Other Options Worth Evaluating

We narrowed the comparison to three categories. Depending on your constraints, also consider:

- [Amazon Neptune](https://docs.aws.amazon.com/neptune/) — managed property graph *and* RDF triplestore in one service; worth a look if you're already committed to AWS.
- [Stardog](https://docs.stardog.com/) — RDF triplestore with a built-in reasoning and virtual-graph layer, positioned for enterprise data-integration use cases.
- [TigerGraph](https://docs.tigergraph.com/) — property graph optimized for large-scale analytical graph queries rather than LLM-orchestration ecosystem support.

## Recommended Startup Path

1. Start with Neo4j and a minimal domain ontology.
2. Add LangChain or LlamaIndex as the orchestration layer.
3. Add vector retrieval only when graph traversal alone is insufficient.
4. Introduce stronger validation and governance as the ontology matures.
