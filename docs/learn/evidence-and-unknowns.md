# Evidence and unknown answers

An answer should identify the assertions that support it, the data version and the limitations. If no supporting assertion is retrieved, return “Insufficient evidence in this dataset.” Do not turn absence into a negative fact and do not let a language model invent a citation.

Use `ontology_starterkit.evidence.build_answer` for this contract. It rejects evidence IDs outside the retrieved set and deduplicates citations.
