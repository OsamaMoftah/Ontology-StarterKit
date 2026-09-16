# Optional adapters

The core kit runs offline with RDFLib and pySHACL. Optional adapters are kept
behind extras so a learner can clone, install and validate a pack without cloud
credentials.

## GraphRAG

Install `pip install -e '.[graphrag]'` and follow the [KG-RAG guide](../../src/integrations/langchain/kg-rag/README.md).
The example requires a Neo4j instance and an LLM key at runtime. Its regex validator catches common unsafe patterns but does not prove a query
is read-only or cheap. Treat this as an experimental example. It needs a
least-privilege Neo4j user, network controls and production query monitoring.

The pinned local service can be started and seeded with `just services-ready`
and `just services-seed`. The seed helper writes `RDFTerm` nodes and
`TRIPLE` relationships, preserving URI resources, blank nodes, and literal
datatype/language metadata after RDFLib parsing. Blank nodes are canonicalized
and scoped to the pack ID. `neo4j_queries.py` provides the normal parameterized
query path with type, predicate, row, byte, and deadline checks; generated
Cypher remains explicitly experimental. The runtime verifier seeds the business
and hello packs, compares the named Neo4j result with RDFLib, checks
language-tagged literals and scoped blank-node identity, repeats an import, and
uses an explicit server transaction timeout. Run it with `just services-runtime`.
The pinned Community image passes those parity and cancellation checks but does
not expose the role-grant command needed to create a database-enforced reader.
`just services-access-control` fails closed with that exact reason; run it
against a licensed Enterprise service to close the read-denial gate.

## MCP

Install `pip install -e '.[mcp]'`. The adapter exposes pack listing, SHACL
validation and manifest-declared named queries over stdio:

```bash
python -c 'from ontology_starterkit.mcp_server import serve; serve("examples")'
```

It does not accept arbitrary SPARQL or write to a graph. Each query call bounds
rows, response bytes, and the local worker deadline; timeout cancellation is a
request boundary, not proof of server-side database cancellation. Add an
authenticated host wrapper before exposing it outside a local development
process. The server also passes its configured `examples` root into every tool,
so a caller cannot ask the adapter to load an arbitrary pack path.

## LinkML and extraction

The `linkml` extra is available for teams that want to continue the generated
schema in LinkML. `build_linkml_schema` creates a deterministic scaffolding
file from a reviewed class-to-slot mapping; it does not invent cardinalities or
semantic mappings.

```python
from ontology_starterkit.linkml import build_linkml_schema
print(build_linkml_schema("hello", {"Person": ["name"]}))
```

The reviewed environment pins the full resolved core and optional dependency
graphs in `requirements/core.lock` and `requirements/optional.lock`. They were
compiled on macOS/Python 3.11; regenerate from the matching `.in` file for a
different platform or interpreter before production use.

The full optional generator check is `python scripts/verify_linkml_generator.py`.
It runs `gen-json-schema --top-class Person --closed` and verifies the checked-in
valid and invalid fixtures.

`ontology_starterkit.extraction` provides a model-independent extraction
contract and reviewed alias resolution; it intentionally does not call an LLM
or merge ambiguous entities. A production extractor must retain source spans,
confidence, model/version metadata and an abstention path.

Only reviewed, locally owned packs should be served. Named queries must be local
SELECT queries; SERVICE, FROM, updates, and other result types are rejected.
The local MCP worker is bounded by a deadline and disposed after each request;
database adapters still need transaction-level timeouts and server-side
cancellation evidence. Path checks are not a defense against someone
concurrently modifying the pack directory.

`build_answer` checks citation membership and records supplied paths. Its
`unverified` status means the text has not been checked for entailment or
source support; a known entity ID alone cannot prove an answer.
