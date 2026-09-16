# Ontology in AI

Knowledge representation predates current language models. Modern GraphRAG systems use graph structure to retrieve or summarize related information, while a curated ontology supplies reviewed meanings and constraints. They are complementary and should not be presented as interchangeable.

Microsoft published its GraphRAG work in 2024. The current kit treats GraphRAG as an optional integration: first validate the semantic model offline, then project a declared subset into a graph store, then return evidence-shaped answers. MCP can expose bounded ontology tools to agents, but it is an integration protocol rather than a new ontology standard.

Sources: [Microsoft GraphRAG](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/), [W3C OWL](https://www.w3.org/TR/owl2-overview/), [W3C SHACL](https://www.w3.org/TR/shacl/).
