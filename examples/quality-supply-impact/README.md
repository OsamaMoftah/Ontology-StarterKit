# Quality and supply change impact

This synthetic pack separates a suggested impact from a reviewed disposition.
`under-review` is not an approval. The records are fictional and await domain
expert review.

```bash
ontokit validate examples/quality-supply-impact
ontokit eval examples/quality-supply-impact impact
```

The pack distinguishes a suggested impact, an under-review disposition, and an
approved disposition. The current records are synthetic and await domain review.

The impact path includes a product, site, supplier, material, process, method,
and filing. It also carries a stale review and an ambiguous identity mapping so
the expected output can separate suggested impact from a review decision and an
approved disposition. No relationship is treated as approved solely because it
is reachable in the graph.
