# Diagram sources

The canonical diagram sources live with each pack so a model, fixture and
visual can be reviewed together. Cross-pack visual stories live under
`infographics/` and authored editorial illustrations under `illustrations/`;
generated output belongs in `media/exports/`.

Run `python scripts/render_diagrams.py` after changing a source and inspect the
SVG title, description and text equivalent before committing it.

Run `python scripts/render_infographics.py` to regenerate the eight teaching
visuals and three consulting visuals from the deterministic visual system.
