# Media helpers

The media layer keeps visual teaching assets reviewable and reproducible:

- `exports/` contains accessible SVG diagrams and infographics.
- `source/` contains canonical diagram sources and rendering notes.
- `manifest.yaml` records provenance, licenses, alt text and the lesson each
  asset supports.

![Ontology delivery lifecycle](exports/ontology-lifecycle.svg)

The lifecycle infographic is a text-equivalent visual: frame a decision, model
terms, validate evidence, connect an optional graph, and maintain the model.
Run `python scripts/render_diagrams.py` to regenerate the pack diagrams.

