# Learn ontologies by running them

The lessons use the bundled packs and do not require a graph database or an API key.

1. [When do you need an ontology?](when-do-you-need-an-ontology.md)
2. [Classes, instances and relations](classes-instances-relations.md)
3. [RDF and stable identifiers](rdf-identifiers.md)
4. [OWL and SHACL](owl-versus-shacl.md)
5. [Competency questions](competency-questions.md)
6. [Evidence and unknown answers](evidence-and-unknowns.md)
7. [Life-science annotations](../../examples/life-science-annotations/README.md)
8. [Consulting evidence rooms](../consulting/README.md)
9. [Infographic lessons](infographics.md)
10. [Workshop stories](../stories/README.md)
11. [Ontology-guided extraction](extraction.md)

Every lesson should end with a command, a deliberate failure, and an explanation of what the result does not prove.

The per-lesson “Try, break, explain” sections are executable teaching contracts. They use synthetic packs, so an applied project must replace the source register, reviewer, and acceptance measure before using the pattern with client or scientific data.

After installing the package, verify the positive commands from a clean checkout with `python scripts/verify_lesson_commands.py`. The verifier uses the active interpreter, writes generated outputs to a temporary directory, and leaves deliberate failure commands for the reader to run separately.
