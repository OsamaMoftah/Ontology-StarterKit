# Visual inspection record

The teaching and consulting SVGs were rendered through the Playwright Chromium
renderer at their intended canvases:

```bash
python scripts/inspect_visuals.py --output-dir /tmp/ontokit-visual-review/renders
```

The check covers 14 desktop compositions at 1400×900, the 1150×385 class-level
consulting model, and 14 dedicated mobile compositions at 390×844. The
rendered contact sheets were inspected at native size for clipping, contrast,
text legibility, arrow collisions, and readable labels. The mobile compositions
use their own 390px layouts; they are not scaled desktop exports.

Observed result: all 29 assets rendered at the declared canvas size. The dark
footer and pale paper background remain distinct at both sizes; relationship
arrows terminate at their intended nodes; the mobile cards keep their text
inside the portrait canvas. The class-level consulting model remains separate
from the instance-level teaching diagrams.

This is a visual acceptance record for the supplied synthetic examples. A
consultancy or scientific team should still review terminology and domain
meaning before using the graphics with client or scientific material.
