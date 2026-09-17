# Ontology reference: consulting-evidence-room

Generated from the canonical Turtle file. Review definitions and constraints before publication.

## Classes

- `https://ontology-starterkit.dev/consulting/Asset` — Asset
- `https://ontology-starterkit.dev/consulting/Claim` — Claim
- `https://ontology-starterkit.dev/consulting/EvidenceRecord` — Evidence record
- `https://ontology-starterkit.dev/consulting/Indication` — Indication
- `https://ontology-starterkit.dev/consulting/Source` — Source

## Properties

- `https://ontology-starterkit.dev/consulting/about` — domain `https://ontology-starterkit.dev/consulting/Claim`, range `https://ontology-starterkit.dev/consulting/Asset`
- `https://ontology-starterkit.dev/consulting/forIndication` — domain `https://ontology-starterkit.dev/consulting/Asset`, range `https://ontology-starterkit.dev/consulting/Indication`
- `https://ontology-starterkit.dev/consulting/fromSource` — domain `https://ontology-starterkit.dev/consulting/EvidenceRecord`, range `https://ontology-starterkit.dev/consulting/Source`
- `https://ontology-starterkit.dev/consulting/name`, range `http://www.w3.org/2000/01/rdf-schema#Literal`
- `https://ontology-starterkit.dev/consulting/publishedOn`, range `http://www.w3.org/2000/01/rdf-schema#Literal`
- `https://ontology-starterkit.dev/consulting/retrievedOn`, range `http://www.w3.org/2000/01/rdf-schema#Literal`
- `https://ontology-starterkit.dev/consulting/reviewState`, range `http://www.w3.org/2000/01/rdf-schema#Literal`
- `https://ontology-starterkit.dev/consulting/reviewedOn`, range `http://www.w3.org/2000/01/rdf-schema#Literal`
- `https://ontology-starterkit.dev/consulting/reviewer`, range `http://www.w3.org/2000/01/rdf-schema#Literal`
- `https://ontology-starterkit.dev/consulting/sourceSpan`, range `http://www.w3.org/2000/01/rdf-schema#Literal`
- `https://ontology-starterkit.dev/consulting/sourceVersion`, range `http://www.w3.org/2000/01/rdf-schema#Literal`
- `https://ontology-starterkit.dev/consulting/supportedBy` — domain `https://ontology-starterkit.dev/consulting/Claim`, range `https://ontology-starterkit.dev/consulting/EvidenceRecord`
- `https://ontology-starterkit.dev/consulting/text`, range `http://www.w3.org/2000/01/rdf-schema#Literal`
