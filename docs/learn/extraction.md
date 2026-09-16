# Ontology-guided extraction

Run `python scripts/run_extraction_lesson.py examples/life-science-annotations/extraction-lesson.yaml`. The fixed passage and restricted vocabulary produce candidates with exact character spans, source IDs, confidence, and model/version metadata. The script builds a proposed RDF diff and checks it against the life-science SHACL shapes, but leaves insertion behind a separate trusted write path.

Break the lesson by changing a candidate span or class ID in a copied fixture. `validate_candidates` rejects the candidate before any diff is reviewable. Ambiguous names, unsupported relationships, invented citations, and live-model output must enter the review queue or abstain. A future model runner may call the same contract; the deterministic fixture is the offline acceptance path.
