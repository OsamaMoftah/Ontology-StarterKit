# Remaining Ontology StarterKit Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the highest-value gaps in U01–U26 with tested offline behavior, explicit live-service boundaries, reproducible artifacts, and an honest evidence matrix.

**Architecture:** Keep the core offline and deterministic. Add bounded named-query contracts, evidence/path verification, entity-resolution and extraction workflows as pure Python modules. Keep Neo4j, MCP, LinkML, and model adapters optional, with live checks isolated behind explicit service tests. Generate visuals from inspectable source data and verify desktop/mobile outputs.

**Tech Stack:** Python 3.10–3.12, RDFLib, pySHACL, Typer, pytest, LinkML runtime, Neo4j driver, MCP, SVG/PNG generation, Markdown, Docker Compose.

## Global Constraints

- Preserve reviewed fixes at `70f1679` and the published `v0.2.0` tag.
- Do not claim live Neo4j, model, scientific, or expert review without fresh evidence.
- Keep generated Cypher experimental; named parameterized queries are the supported path.
- Preserve synthetic/fictional labels and source/license metadata.
- Every implementation change gets a failing regression test first, then a focused passing test.
- Update the U01–U26 evidence matrix after each workstream.

---

### Task 1: Reproducible core and manifest contracts

**Files:** `src/ontology_starterkit/packs.py`, `src/ontology_starterkit/validation.py`, `tests/unit/test_packs.py`, `tests/semantic/test_domain_packs.py`, `requirements/*.txt`, `.github/workflows/python-checks.yml`.

- [ ] Add manifest version, required-field, path-type, query/fixture, and target-coverage checks.
- [ ] Add negative fixtures for empty/unrelated graphs and assert failure reasons.
- [ ] Add lock files and fresh-install CI checks.
- [ ] Verify core and optional environments on Python 3.10, 3.11, and 3.12.
- [ ] Commit `feat: enforce pack contracts and reproducible core installs`.

### Task 2: Safe named query and Neo4j execution contract

**Files:** `src/ontology_starterkit/neo4j_queries.py`, `src/ontology_starterkit/neo4j_runtime.py`, `scripts/seed_neo4j.py`, `tests/unit/test_neo4j_queries.py`, `tests/integration/test_neo4j_runtime.py`, `docs/reference/optional-adapters.md`.

- [ ] Add a named Cypher template registry with typed parameter schemas and allowlisted values.
- [ ] Reject syntax interpolation, unknown parameters, writes, procedures, and unbounded patterns.
- [ ] Add row, byte, deadline, and result serialization limits.
- [ ] Add server-side transaction timeout and cancellation evidence for a live Neo4j profile.
- [ ] Test literal metadata, scoped blank nodes, repeated imports, changed imports, and stale-fact deletion.
- [ ] Commit `feat: add bounded named Neo4j query runtime`.

### Task 3: Evidence, evaluation, entity resolution, and extraction

**Files:** `src/ontology_starterkit/evidence.py`, `src/ontology_starterkit/evals.py`, `src/ontology_starterkit/entity_resolution.py`, `src/ontology_starterkit/extraction.py`, `tests/unit/test_evidence.py`, `tests/unit/test_entity_resolution.py`, `tests/unit/test_extraction.py`, `examples/business-projects/*`.

- [ ] Verify supplied graph paths against triples and source spans.
- [ ] Add supported, unsupported, conflicting, stale, and unknown evaluation fixtures.
- [ ] Add reversible alias decisions and an explicit review queue for ambiguous matches.
- [ ] Add deterministic constrained extraction with validated character spans and review diffs.
- [ ] Add SHACL-gated candidate validation without automatic insertion.
- [ ] Commit `feat: add reviewable evidence and identity workflows`.

### Task 4: Life-science and consulting domain depth

**Files:** `examples/life-science-annotations/*`, `examples/consulting-evidence-room/*`, `examples/quality-supply-impact/*`, `docs/consulting/*`, `docs/history/*`.

- [ ] Add versioned, licensed, provenance-rich synthetic/source-separated annotation records.
- [ ] Add conflicting, stale, ambiguous, and species-sensitive evidence cases.
- [ ] Add a seven-question therapeutic evidence decision packet generator.
- [ ] Add the synthetic quality/supply change-impact pack with review-state distinctions.
- [ ] Expand all 12 consulting rows into engagement cards and templates.
- [ ] Commit `feat: expand life-science and consulting workflows`.

### Task 5: ROI, LinkML, ontology reference, and migration tooling

**Files:** `src/ontology_starterkit/roi.py`, `src/ontology_starterkit/linkml.py`, `scripts/generate_reference.py`, `scripts/check_migration.py`, `tests/unit/test_roi.py`, `tests/unit/test_linkml.py`, `docs/reference/*`, `docs/governance/*`.

- [ ] Add executable ROI scenarios, zero-rate NPV, no-payback, sensitivity, and double-counting checks.
- [ ] Add LinkML cardinality/enums/identifier conversion and equivalence fixtures.
- [ ] Generate ontology reference output from canonical Turtle and document limitations.
- [ ] Add a compatible and breaking ontology migration benchmark.
- [ ] Commit `feat: add executable ROI reference and migration tooling`.

### Task 6: Visual and curriculum completion

**Files:** `scripts/render_infographics.py`, `media/source/infographics/*`, `media/exports/*`, `media/manifest.yaml`, `docs/learn/*`, `docs/consulting/*`.

- [ ] Add dedicated 390px compositions for every teaching visual.
- [ ] Add claim-trace, identity-crosswalk, and quality-impact consulting visuals.
- [ ] Add per-asset provenance, captions, review state, and exercise metadata.
- [ ] Add deliberate failures and solutions to every beginner lesson.
- [ ] Rasterize and inspect desktop/mobile outputs for clipping, contrast, and legibility.
- [ ] Commit `feat: complete mobile visuals and learning exercises`.

### Task 7: Final evidence and delivery

**Files:** `docs/reviews/2026-09-16-luna-review.md`, `README.md`, `.github/workflows/*`, `CHANGELOG.md`.

- [ ] Run core, optional, MCP, Neo4j, wheel, visual, link, type, lint, and audit checks.
- [ ] Mark each U01–U26 item implemented, verified, partial, or externally blocked with evidence.
- [ ] Confirm hosted CI and preserve `v0.2.0`.
- [ ] Commit `docs: publish final upgrade evidence matrix`.
