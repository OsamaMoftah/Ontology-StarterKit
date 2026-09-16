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

The `bad-relation.ttl` and `missing-name.ttl` files are deliberately invalid. Removing a manager assertion creates an **unknown** answer; it does not prove that no manager exists. All data is fictional and CC0-1.0.
