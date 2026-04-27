# Ontology StarterKit Decision Framework

Choosing the right storage and query model is one of the most important design decisions in an ontology-backed AI system.

## Quick Recommendation

| Primary goal | Recommended path | Why |
| :--- | :--- | :--- |
| GraphRAG for GenAI products | Property graph such as Neo4j | Strong developer tooling and ecosystem support for LangChain and LlamaIndex integrations |
| Heavy reasoning and strict semantic governance | RDF triplestore such as GraphDB or RDFox | Best support for OWL, SHACL, and standards-first validation |
| Search-led product with light graph filtering | Hybrid vector-graph system such as Weaviate | Supports semantic retrieval with lighter-weight relationship constraints |

## Comparison Matrix

| Feature | Property Graph | RDF Triplestore | Hybrid Vector-Graph |
| :--- | :--- | :--- | :--- |
| Query language | Cypher | SPARQL | Vendor-specific APIs |
| LLM integration maturity | High | Lower | High |
| OWL reasoning | Low to moderate | High | Low |
| SHACL-native governance | Low | High | Low |
| Learning curve | Moderate | High | Low to moderate |
| Best fit | Product teams building GraphRAG quickly | Regulated or standards-heavy environments | Search-first AI products |

## Practical Rule of Thumb

- Start with a property graph if your immediate goal is an LLM-facing product feature.
- Choose RDF first if your main constraint is semantic rigor, validation, or standards compliance.
- Use a hybrid vector-graph store when semantic search is dominant and graph structure is secondary.

## Recommended Startup Path

1. Start with Neo4j and a minimal domain ontology.
2. Add LangChain or LlamaIndex as the orchestration layer.
3. Add vector retrieval only when graph traversal alone is insufficient.
4. Introduce stronger validation and governance as the ontology matures.
