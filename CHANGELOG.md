# Changelog

## Versioning Policy

Ontology StarterKit follows Semantic Versioning:

- `MAJOR`: Breaking changes to public behavior, CLI contracts, or repository usage expectations.
- `MINOR`: Backward-compatible features and workflow additions.
- `PATCH`: Backward-compatible fixes, hardening, and documentation corrections.

For ontology updates, include a short impact statement in the release notes (for example: validation-only change, schema extension, or breaking semantic change).

## Unreleased

- Added a visual system with eight accessible ontology explainers, three life-science consulting visuals, a gallery, editable source specs and two original editorial illustrations.
- Rewrote Mermaid rendering to preserve dotted instance edges, branch topology, wrapped labels, and accessible title/description IDs; unsupported edges now fail loudly.
- Expanded every domain pack to at least five named competency questions (seven for the consulting pack) with expected fixtures.
- Hardened CLI failure codes, Unicode-safe alias resolution, evidence-path checks, unsafe SPARQL rejection, MCP path boundaries, and lossless RDF term seeding.
- Added sourced ontology history, fictional business and life-science workshop stories, a deterministic Markdown link checker, and core-only optional-dependency skips.
- Tightened public documentation wording around the ontology examples without changing their schema or data contracts.

## 0.2.0 - 2026-09-16

- Added an offline CLI for discovering packs, SHACL validation, named queries and fixture evaluations.
- Added self-contained hello, business-project, life-science annotation and consulting evidence-room packs with invalid fixtures, evidence metadata and competency questions.
- Added deterministic evidence, extraction-contract and reviewed alias helpers, plus an optional bounded MCP adapter.
- Added opt-in local Neo4j Compose readiness and idempotent, local-only RDF seed commands.
- Added PyYAML type stubs to the development environment so CI type checks are consistent across Python versions.
- Added accessible SVG diagram generation, learning lessons, ontology history, glossary and a 12-case life-sciences consulting catalogue.
- Added packaging, Ruff, mypy, Just, citation, issue-template and ownership metadata for maintainers.
- Hardened the optional LangChain/Neo4j example against procedure calls, unbounded paths, Cartesian patterns, ambient settings and timeout leaks.

- Fixed broken `file://` links in `docs/for-startups/30-day-sprint.md` and `docs/for-product-managers/roi-calculator/README.md` that pointed to a contributor's local filesystem path.
- Corrected the ROI template's cost model: `C_upfront` is now explicitly derived from build-phase costs, the worked example's Executive Summary Table now reconciles arithmetically with the stated formulas, and payback period is no longer shown as horizon-dependent.
- Added sourced links and an explicit "opinionated default, not a benchmark" framing to the decision framework, and reconciled its OWL-reasoning claims with the fact this repo's shipped ontology example is SHACL-only.
- Added `docs/README.md` as a documentation index and cross-linked the product-manager templates to each other.
- Reframed the 30-day sprint guide as a suggested plan rather than an implied case study.

## 0.1.0 - 2026-04-27

- Renamed the project to Ontology StarterKit and aligned repository-facing terminology with the new identity.
- Added open-source publication essentials, including licensing, contribution guidance, a code of conduct, a security policy, `.gitignore`, and `.env.example`.
- Refined the LangChain KG-RAG example with stronger configuration handling, structured logging, validation guardrails, and comprehensive docstrings.
- Added runnable ontology assets, automated tests, and CI workflows that validate both Python and ontology components.
- Revised documentation so user-facing guidance is precise, technically accurate, and consistent with the implemented repository state.
