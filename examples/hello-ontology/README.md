# Hello Ontology

This pack is a small, offline-first lesson. Maya Chen manages Team Aurora, and Team Aurora works on Alpha Project. The model, instance data, SHACL requirements, named SPARQL question, expected answer and evidence identifiers are separate artifacts.

```bash
ontokit packs
ontokit validate examples/hello-ontology
```

Validate with pySHACL:

```bash
pyshacl -s examples/hello-ontology/shapes.ttl examples/hello-ontology/data/valid.ttl
```

The `bad-relation.ttl` and `missing-name.ttl` files are invalid fixtures. The lesson cases in `data/cases/` show the safe answer contract: removing a manager assertion creates an **unknown** answer, while two managers create an **ambiguous** answer. Neither case is silently converted into a confident name. All data is fictional and CC0-1.0.
