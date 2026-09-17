# RDF and stable identifiers

RDF represents a statement as subject, predicate and object. IRIs identify resources; labels are readable properties and can change. The packs use `https://ontology-starterkit.dev/...` identifiers so the same entity can be referred to across files without relying on its display name.

Avoid using a name as an identity key. A mapping from two source records to one canonical entity is a reviewed assertion with provenance. Preserve the source identifiers and the mapping decision.

## Try, break, explain

Run `python -m ontology_starterkit.cli query examples/business-projects owner` to see stable IRIs in the result. Break the identity assumption by creating two source rows with the same display name; the entity-resolution exercise queues the collision rather than merging it. A stable IRI makes a reference repeatable, but it does not make a mapping correct without review.
