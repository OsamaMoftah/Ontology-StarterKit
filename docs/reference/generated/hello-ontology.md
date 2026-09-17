# Ontology reference: hello-ontology

Generated from the canonical Turtle file. Review definitions and constraints before publication.

## Classes

- `https://ontology-starterkit.dev/hello/EvidenceRecord` — Evidence record
- `https://ontology-starterkit.dev/hello/Person` — Person
- `https://ontology-starterkit.dev/hello/Project` — Project
- `https://ontology-starterkit.dev/hello/Team` — Team

## Properties

- `https://ontology-starterkit.dev/hello/manages` — domain `https://ontology-starterkit.dev/hello/Person`, range `https://ontology-starterkit.dev/hello/Team`
- `https://ontology-starterkit.dev/hello/name`, range `http://www.w3.org/2000/01/rdf-schema#Literal`
- `https://ontology-starterkit.dev/hello/supportedBy`, range `https://ontology-starterkit.dev/hello/EvidenceRecord`
- `https://ontology-starterkit.dev/hello/worksOn` — domain `https://ontology-starterkit.dev/hello/Team`, range `https://ontology-starterkit.dev/hello/Project`
