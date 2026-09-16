# Ontology Starter Kit Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Turn the repository from a single tutorial into a visually strong, testable ontology starter kit for AI engineers, ontology practitioners, and life-science consultancies.

**Architecture:** Keep the offline RDF/SHACL/SPARQL core dependency-light; make Mermaid rendering and infographic generation deterministic and inspectable; add consulting stories and source-backed learning content around the same pack contracts. Optional GraphRAG and Neo4j adapters remain isolated and fail closed.

**Tech Stack:** Python 3.11+, RDFLib, pySHACL, Typer, pytest, Ruff, mypy, dependency-free SVG, Markdown, Mermaid source, Docker Compose.

> Status: this is the intended scope, not a completion report. See the
> [independent review](../../reviews/2026-09-16-luna-review.md) for verified delivery and remaining gates.

## Global Constraints

- Preserve the four existing example packs and their offline-first behavior.
- Every visual must have an editable source, accessible SVG metadata, accurate labels, and a text equivalent.
- Named queries are allowlisted and unsafe SPARQL operations are rejected.
- Core-only installation must collect and run tests without optional GraphRAG dependencies.
- Claims in history and consulting material must be sourced or explicitly marked fictional.

### Task 1: Correct the Mermaid renderer

Files: `scripts/render_diagrams.py`, `tests/unit/test_render_diagrams.py`.

Write failing tests for dotted edges, branch-safe layered layout, wrapped labels, resolved title/description IDs, and unsupported edge diagnostics. Rewrite the parser to retain display labels and edge kinds, lay out a DAG by levels, render solid and dotted paths with accessible metadata, and fail visibly on unsupported edge syntax. Run the focused tests, then regenerate the pack SVGs.

### Task 2: Harden core contracts

Files: `src/ontology_starterkit/cli.py`, `src/ontology_starterkit/extraction.py`, `src/ontology_starterkit/validation.py`, `src/ontology_starterkit/evidence.py`, `src/ontology_starterkit/mcp_server.py`, `scripts/seed_neo4j.py` plus focused unit tests.

Add nonzero CLI exits for invalid validation and failed evaluations; preserve Unicode identifiers and reject alias collisions; constrain alias application to requested fields and expose audit changes; reject unsafe SPARQL operations; constrain MCP pack paths to an examples root; require evidence paths for cited claims; represent RDF literals separately in Neo4j seed output. Test each behavior before implementation and run the full unit suite.

### Task 3: Build the visual system

Files: `scripts/render_infographics.py`, `media/source/infographics/*.yaml`, `media/exports/infographic-*.svg`, `media/gallery.md`, `media/manifest.yaml`, `docs/learn/infographics.md`.

Create eight editorial infographics covering definitions, graph layers, OWL versus SHACL, question-to-evidence, unknown versus false, reuse, life-science annotation, and term migration. Add three consulting visuals for a value chain, evidence room, and pilot scorecard. Use a shared palette and typography, curved relationship paths, comparison compositions, accurate text, accessible metadata, and source specs. Add the gallery and text equivalents.

### Task 4: Add authored illustrations and stories

Files: `media/source/illustrations/*`, `docs/history/timeline.md`, `docs/stories/*.md`, `docs/learn/README.md`, `README.md`.

Add a coherent generated hero and supporting illustration assets with provenance metadata. Expand ontology history into a sourced multi-lane timeline and add fictional but realistic business, consulting, and life-science stories with runnable links to packs and explicit evidence limits.

### Task 5: Expand packs and developer experience

Files under `examples/*`, `.github/workflows/python-checks.yml`, `scripts/check_links.py`, `tests/unit/test_check_links.py`, `README.md`.

Give each pack at least five meaningful competency questions (seven for consulting), expected fixtures, and invalid fixtures. Add a deterministic Markdown link checker to CI, document optional dependency skips, and add reproducible local commands for rendering, validation, queries, and evaluation.

### Task 6: Verify and deliver

Run focused tests after each task, then `ruff check`, `mypy`, core-only pytest, optional GraphRAG pytest, pack validation/evaluation, link checks, SVG/XML checks, and build/audit commands. Inspect representative visuals at desktop and mobile widths. Commit the branch, push it, and open a reviewable PR with an evidence matrix and explicit remaining gates.
