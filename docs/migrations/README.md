# Semantic migration benchmark

The [`0.2-to-0.3.yaml`](0.2-to-0.3.yaml) fixture classifies two queries that should continue to work, one query that needs review, and a property replacement. Reproduce the compatibility check from the repository root:

```bash
python scripts/check_migration.py docs/migrations/0.2-to-0.3.yaml \
  --query manager --query owner --query evidence
```

The safe change keeps identifiers and query bindings stable. The breaking change replaces `owns` with `ownsAsset`; migrate stored triples and update the named query before accepting the new model. Release notes must publish the replacement, deprecation window, package version, and compatibility output together. The published `v0.2.0` tag remains the old landing point.
