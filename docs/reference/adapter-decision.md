# Additional adapter decision

U23 remains deferred. The core and Neo4j paths already cover the reviewed offline and graph workflows; adding another store without a named maintainer, test dataset, and user demand would increase the maintenance surface without improving the starter path. A new adapter may enter when a contributor supplies:

- one concrete decision that the current paths cannot support;
- a named maintenance owner and supported version range;
- the same competency-question, provenance, row-limit, and answer-support contract;
- an integration fixture that can run in CI or is clearly marked externally blocked.

Until that gate is met, the status is deferred rather than an inflated adapter count.

## Hybrid retrieval lesson

Use lexical retrieval for exact identifiers and terminology, vector retrieval for paraphrases, and graph traversal for typed relationships and provenance. Combine them only when an evaluation set shows a measurable recall or review-time gain. The returned candidates must still pass the same source-span, graph-path, freshness, and answer-support checks; retrieval score is not evidence of correctness.
