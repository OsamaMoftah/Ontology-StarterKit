# Ontology StarterKit Upgrade Implementation Plan

> **For agentic workers:** Implement task-by-task with test-first verification and keep each slice reviewable.

**Goal:** Turn Ontology StarterKit into a reproducible, offline-first ontology learning and implementation kit with safe optional GraphRAG, business/life-science consulting packs, visual helpers, and maintainable public-project workflows.

**Architecture:** A small Python package owns pack discovery, RDF/SHACL validation, named competency queries, evidence-shaped answers, deterministic diagrams, and optional integrations. Domain packs are self-contained and manifest-driven. Service-dependent Neo4j/LLM/MCP features remain explicit extras and never define the offline first-run path.

**Tech Stack:** Python 3.10+, RDFLib, pySHACL, SPARQL, Typer, Pydantic, pytest, Ruff, mypy; optional Neo4j/LangChain, LinkML, MCP and Docker extras.

## Global Constraints

- No committed credentials, proprietary data, or unlicensed ontology extracts.
- Offline core must run without Neo4j, an LLM, or network access.
- Generated answers must expose supporting evidence IDs or abstain.
- Domain packs must carry sources, versions, licenses, invalid fixtures and competency questions.
- Do not claim clinical, legal, regulatory, security, or financial outcomes without evidence and qualified review.
- Maintain existing MIT code license; license original media separately where appropriate.

---

### Task 1: Package and offline CLI foundation

**Files:** create `pyproject.toml`, `src/ontology_starterkit/__init__.py`, `src/ontology_starterkit/cli.py`, `src/ontology_starterkit/packs.py`, `tests/unit/test_packs.py`; modify `.gitignore` if needed.

Implement a Typer CLI with `ontokit packs`, `ontokit validate <pack>`, and `ontokit query <pack> <query_id>`. Keep pack loading deterministic and path-safe. Tests must cover discovery, missing manifest errors, valid/invalid validation, named-query parameter rejection and JSON output.

### Task 2: Complete the Hello Ontology pack

**Files:** create `examples/hello-ontology/manifest.yaml`, `ontology.ttl`, `shapes.ttl`, `data/valid.ttl`, `data/invalid/missing-name.ttl`, `data/invalid/bad-relation.ttl`, `queries/manager.rq`, `questions.yaml`, `expected/manager.json`, `sources.yaml`, `model.mmd`, `README.md`; create `tests/semantic/test_hello_pack.py`.

Model Person, Team, Project, `manages`, `worksOn`, names and provenance. Add tests for both invalid fixtures, empty-target protection, named query result and unknown-answer behavior.

### Task 3: Consulting and life-science packs

**Files:** create `examples/business-projects/*`, `examples/life-science-annotations/*`, `examples/consulting-evidence-room/*`; create `tests/semantic/test_domain_packs.py`; modify `docs/README.md`.

Use synthetic business/consulting data and a small explicitly attributed GO-inspired teaching dataset without redistributing restricted content. Each pack must use the same manifest contract and include evidence, source versions, competency questions, negative fixtures and diagrams.

### Task 4: Harden optional GraphRAG integration

**Files:** create `tests/unit/test_graph_rag_safety.py`; modify `src/integrations/langchain/kg-rag/graph_rag.py`, README, requirements and `.env.example`.

Replace substring-only acceptance with a conservative read-only policy: reject procedures and unrestricted patterns by default, require a single statement and a bounded projection/limit. Validate positive identifiers/literals. Configure explicit graph transaction timeout and finite retries; distinguish `None` from an empty env mapping and reject invalid/placeholder settings.

### Task 5: Packaging, lint, typing and service development

**Files:** create `ruff.toml`, `mypy.ini`, `justfile`, `.devcontainer/devcontainer.json`, `docker-compose.yml`; modify workflows and CONTRIBUTING.

Core installation must not install optional service dependencies. Add CI for tests, Ruff, mypy, pack validation and link checks. Compose is opt-in, local-only and version-pinned; provide readiness and seed commands.

### Task 6: Visual helpers and documentation

**Files:** create `media/manifest.yaml`, `media/source/hello-model.mmd`, `media/source/README.md`, `scripts/render_diagrams.py`, `docs/learn/*`, `docs/history/*`, `docs/consulting/*`, `assets/README.md`; modify root README and docs index.

Generate deterministic SVG from reviewed Mermaid/source fixtures where tooling is available; always include text equivalents and alt text. Add sourced history, consulting path, glossary and runnable lesson sequence.

### Task 7: Evidence answers and evaluation

**Files:** create `src/ontology_starterkit/evidence.py`, `src/ontology_starterkit/evals.py`, `evals/questions.yaml`, `evals/README.md`, `tests/unit/test_evidence.py`.

Return structured answer records with `answer`, `evidence_ids`, `data_version`, `status` and `limitations`. Add offline evaluation for exact bindings, abstention and citation membership.

### Task 8: Optional extraction, LinkML and MCP adapters

**Files:** create `src/ontology_starterkit/extraction.py`, `src/ontology_starterkit/mcp_server.py`, `docs/reference/optional-adapters.md`, tests for deterministic candidate extraction and bounded named tools; add optional dependency groups.

Start with local deterministic interfaces. No arbitrary remote query, file access, network import or unrestricted writes. Mark these features experimental until tests and documentation are complete.

### Task 9: Public release and maintenance

**Files:** create issue forms, CODEOWNERS, CITATION.cff, release workflow/docs, media attribution and source manifests; update CHANGELOG and README.

Run all checks from a clean checkout, publish a tagged release, and report local/CI/service boundaries separately.

