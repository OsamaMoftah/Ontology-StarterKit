# Optional adapters

The core kit runs offline with RDFLib and pySHACL. Optional adapters are kept
behind extras so a learner can clone, install and validate a pack without cloud
credentials.

## GraphRAG

Install `pip install -e '.[graphrag]'` and follow the [KG-RAG guide](../../src/integrations/langchain/kg-rag/README.md).
The example requires a Neo4j instance and an LLM key at runtime. Its validator
accepts only read-only, bounded Cypher and the application still needs a
least-privilege Neo4j user, network controls and production query monitoring.

The pinned local service can be started and seeded with `just services-ready`
and `just services-seed`. The seed helper writes lossless `RDFTerm` nodes and
`TRIPLE` relationships, preserving URI resources, blank nodes, and literal
datatype/language metadata. It refuses non-local URIs and never drops data.

## MCP

Install `pip install -e '.[mcp]'`. The adapter exposes pack listing, SHACL
validation and manifest-declared named queries over stdio:

```bash
python -c 'from ontology_starterkit.mcp_server import serve; serve("examples")'
```

It does not accept arbitrary SPARQL or write to a graph. Add an authenticated
host wrapper before exposing it outside a local development process. The server
also passes its configured `examples` root into every tool, so a caller cannot
ask the adapter to load an arbitrary pack path.

## LinkML and extraction

The `linkml` extra is available for teams that want to continue the generated
schema in LinkML. `build_linkml_schema` creates a deterministic scaffolding
file from a reviewed class-to-slot mapping; it does not invent cardinalities or
semantic mappings.

```python
from ontology_starterkit.linkml import build_linkml_schema
print(build_linkml_schema("hello", {"Person": ["name"]}))
```

`ontology_starterkit.extraction` provides a model-independent extraction
contract and reviewed alias resolution; it intentionally does not call an LLM
or merge ambiguous entities. A production extractor must retain source spans,
confidence, model/version metadata and an abstention path.
