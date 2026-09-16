# Chowlk authoring and semantic review

The small [`claim-evidence.drawio`](chowlk-fixtures/claim-evidence.drawio) fixture shows two class boxes and a subclass relation.  Chowlk converts that diagrams.net source into OWL/Turtle; the checked-in [`expected.ttl`](chowlk-fixtures/expected.ttl) records the semantic contract that matters to this starter kit:

- `ex:Claim` and `ex:Evidence` remain OWL classes;
- `ex:Claim rdfs:subClassOf ex:Evidence` is preserved;
- labels are retained as editorial annotations.

Run the offline contract check with:

```bash
uv run python scripts/verify_chowlk_conversion.py
```

For a real conversion against the hosted Chowlk service, use:

```bash
uv run python scripts/verify_chowlk_conversion.py --live
```

The live check rejects diagram errors and computes a semantic diff with RDFLib.  It deliberately ignores generated ontology headers, prefixes, and layout metadata.  The canonical Turtle and SHACL models remain authoritative: Chowlk is an authoring aid, and generated IRIs, domains, ranges, cardinalities, restrictions, and annotations still require semantic review.  The conversion was checked against the upstream [Chowlk converter](https://github.com/oeg-upm/Chowlk); the service documents the same diagrams.net-to-OWL workflow.
