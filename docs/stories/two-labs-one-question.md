# Two labs, one question

Two fictional research groups asked whether a gene product participated in a
biological process. Lab A had an annotation and a PMID. Lab B had the same label
but a different species and evidence code. A label-only merge made the result
look stronger than either source supported.

The team modelled the annotation as an entity with a subject, process, taxon,
reference, evidence code, and review status. The graph could answer which
annotations were reviewed for the requested species. It could not decide whether
the biology was true; that remained a scientist's responsibility.

Use the [life-science pack](../../examples/life-science-annotations/README.md)
and its [annotation visual](../../media/exports/infographic-life-science-evidence.svg).
The pack currently links annotations to products, processes, and references;
species filtering and cross-lab reconciliation are not implemented.
The fixture is GO-inspired teaching data, not a redistributed database extract,
and it must never be used for diagnosis or treatment.
