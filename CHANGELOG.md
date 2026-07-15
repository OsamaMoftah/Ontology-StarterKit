# Changelog

## Versioning Policy

Ontology StarterKit follows Semantic Versioning:

- `MAJOR`: Breaking changes to public behavior, CLI contracts, or repository usage expectations.
- `MINOR`: Backward-compatible features and workflow additions.
- `PATCH`: Backward-compatible fixes, hardening, and documentation corrections.

For ontology updates, include a short impact statement in the release notes (for example: validation-only change, schema extension, or breaking semantic change).

## Unreleased

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
