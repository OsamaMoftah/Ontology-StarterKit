# Reference generation and visual authoring

The canonical source for each pack is its `ontology.ttl`; generated Markdown references live in [`generated/`](generated/). Rebuild them with:

```bash
for p in examples/*/ontology.ttl; do id=$(basename "$(dirname "$p")"); python scripts/generate_reference.py "$p" "docs/reference/generated/$id.md"; done
```

The generator lists classes, properties, identifiers, domains, and ranges. It does not replace semantic review of definitions, constraints, mappings, or licensing.

## Chowlk handoff

For a small visual authoring experiment, draw this class/property pair in a Chowlk-compatible diagram:

```text
[Claim] --supportedBy--> [EvidenceRecord]
[EvidenceRecord] --fromSource--> [Source]
```

Export the diagram to Turtle, compare the result with `examples/consulting-evidence-room/ontology.ttl`, and review every generated IRI, domain, range, and cardinality before committing it. Chowlk conversion can lose layout annotations, labels, restrictions, or naming intent; the canonical Turtle and SHACL files remain authoritative.
