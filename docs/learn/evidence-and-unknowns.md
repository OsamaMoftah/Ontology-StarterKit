# Evidence and unknown answers

An answer should identify the assertions that support it, the data version and the limitations. If no supporting assertion is retrieved, return “Insufficient evidence in this dataset.” Do not turn absence into a negative fact and do not let a language model invent a citation.

Use `ontology_starterkit.evidence.build_answer` for this contract. It rejects evidence IDs outside the retrieved set and deduplicates citations.

The helper returns `unverified` for cited text: ID membership and supplied paths
do not establish that the text follows from the graph or its source records.
It returns `insufficient-evidence` when citations or requested paths are missing.

## Try, break, explain

Run `python -m ontology_starterkit.cli eval examples/consulting-evidence-room claim-status` and inspect the explicit `has-evidence` and `no-evidence` rows. Then call `build_verified_answer` with a citation whose graph path is absent; it returns `insufficient-evidence` even when the caller supplied an entity ID. This checks graph-path membership, not whether a source document is scientifically or legally authoritative.
