# RDF and stable identifiers

RDF represents a statement as subject, predicate and object. IRIs identify resources; labels are readable properties and can change. The packs use `https://ontology-starterkit.dev/...` identifiers so the same entity can be referred to across files without relying on its display name.

Avoid using a name as an identity key. A mapping from two source records to one canonical entity is a reviewed assertion with provenance. Preserve the source identifiers and the mapping decision.
