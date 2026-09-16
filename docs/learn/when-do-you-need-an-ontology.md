# When do you need an ontology?

Use a plain table or API schema when one team owns the data, the meanings are stable, and the main task is record storage. Use a controlled vocabulary or SKOS concept scheme when you mainly need labels, broader/narrower concepts and mappings. Consider an ontology when several parties need to agree on concepts and relationships, combine datasets, ask relationship questions, or reason over declared semantics.

An ontology is not automatically better. Ask which decision it improves, who will maintain the definitions, what evidence is available, and whether SQL, a glossary or an ordinary search index would solve the problem more simply.

Try the first pack:

```bash
python -m ontology_starterkit.cli packs
python -m ontology_starterkit.cli validate examples/hello-ontology
```

The commands prove that a pack is discoverable and its declared paths exist. They do not prove the model fits a real organization.
