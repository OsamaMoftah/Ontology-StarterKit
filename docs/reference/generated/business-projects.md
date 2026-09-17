# Ontology reference: business-projects

Generated from the canonical Turtle file. Review definitions and constraints before publication.

## Classes

- `https://ontology-starterkit.dev/business/Person` — Person
- `https://ontology-starterkit.dev/business/Project` — Project
- `https://ontology-starterkit.dev/business/Service` — Service
- `https://ontology-starterkit.dev/business/Team` — Team

## Properties

- `https://ontology-starterkit.dev/business/manages` — domain `https://ontology-starterkit.dev/business/Person`, range `https://ontology-starterkit.dev/business/Team`
- `https://ontology-starterkit.dev/business/name`, range `http://www.w3.org/2000/01/rdf-schema#Literal`
- `https://ontology-starterkit.dev/business/owns` — domain `https://ontology-starterkit.dev/business/Team`, range `https://ontology-starterkit.dev/business/Service`
- `https://ontology-starterkit.dev/business/worksOn` — domain `https://ontology-starterkit.dev/business/Team`, range `https://ontology-starterkit.dev/business/Project`
