# Independent review of the visual and editorial upgrade

Reviewed: 16 September 2026. Baseline: `d15b6d5`; Luna's visual head:
`5897d0a`; editorial head: `dc84af1`. This review covers the combined diff,
its executable paths, documentation claims, diagrams, and older open branches.

The upgrade is useful, but the earlier completion claims exceeded the evidence.
Four packs, 22 queries, eight teaching graphics, three consulting graphics,
two illustrations, and three fictional stories exist. That does not complete
the original U01–U26 plan. Several tests checked presence rather than behavior.

## Findings fixed before merge

| Severity | Finding | Correction / evidence |
| --- | --- | --- |
| High | MCP rejected legitimate immediate-child packs because it required two path components | One component accepted; relative pack names resolve under the configured root; helper and real stdio tests |
| High | Discovery and manifest symlinks could read outside the intended directory | Resolve and check discovered directories and the manifest itself; escape regressions |
| High | SPARQL regex missed `FROM` dataset loading and accepted unsupported result types | Parse syntax; permit one SELECT; reject SERVICE, dataset clauses, updates, and non-row result types; literals/comments remain valid |
| High | Citation membership was labeled `supported`, even for unrelated invented text | Return `unverified`; retain an explicit limitation; paths are recorded, not evidence of entailment |
| High | Generated Cypher was presented as safely bounded | Require experimental CLI opt-in, disable hidden transport retries, document missing result/work bounds and server-cancellation evidence |
| Medium | OWL illustration implied every Person is a Manager | Manager is the subclass; Maya being a Manager entails Maya being a Person |
| Medium | Annotation picture linked evidence to the biological process and used an inappropriate relation | Branch evidence from the annotation; use “about process” from annotation to process; mark the example synthetic |
| Medium | “Inactive” was treated as general logical false | Show an explicit boolean value for `active`; distinguish absence from false for the same property |
| Medium | SVG newlines collapsed; narrow cards overflowed; cobalt nodes had poor contrast | Render wrapped lines separately, use white text on cobalt, inspect raster exports; label scorecard numbers hypothetical |
| Medium | Mermaid parser silently truncated chained edges and fabricated layouts for cycles | Full-line parsing; reject unsupported syntax and cycles |
| Medium | Neo4j blank-node IDs changed between parses and could collide across packs | Canonicalize graph blank nodes and scope them by pack ID; stable/repeated and cross-pack tests |
| Medium | LinkML scaffold used the LinkML namespace for domain classes and omitted imported string types | Local prefix plus `linkml:types`; SchemaView smoke check |
| Medium | Evaluations ignored duplicate result rows | Compare multisets rather than sets |
| Medium | Four question labels promised relationships while queries only listed entity types | Add relationship joins and negative tests with unrelated records; claim-status now returns explicit evidence-link status |
| Medium | `python -m ontology_starterkit.cli` silently did nothing | Module entry point and subprocess regression |
| Medium | Governance changelog gate ignored the new packs | Include `examples/**` in the gate |
| Low | Prose lint became a word ban, including code | Advisory CI, skip fenced code, remove the whole-repository zero-findings assertion |
| Low | Markdown link checker truncated parentheses and paths with spaces | Balanced destinations and angle-bracket handling, with regressions |
| Low | Investment template promised outcomes; sprint confused operational metrics with ROI inputs | Baseline/target/owner table; distinguish measured operating metrics from monetized assumptions |
| Low | Stories implied the packs implemented full reconciliation/reviewer workflows | State which parts are fictional proposed extensions |

## What remains from the original plan

“Partial” means some useful work exists, but its original acceptance gate is not
met. Optional integrations are experiments, not production-ready adapters.

| ID | Status | Evidence or remaining gate |
| --- | --- | --- |
| U01 | Partial | Offline named SPARQL exists. GraphRAG still generates Cypher; no parameterized Neo4j template suite or live write-denial evidence. |
| U02 | Partial | Call counters and client timeouts exist; retries disabled. No query CPU sandbox, byte/token limits, or proven server cancellation. |
| U03 | Partial | Core/extra separation and Python 3.10–3.12 CI; dependency ranges are not reproducible lockfiles. |
| U04 | Implemented, basic | Four manifests separate ontology, shapes, data, questions, sources and diagrams; stricter manifest schemas remain useful. |
| U05 | Partial | Manager query and expected answer run; stronger unknown/ambiguous cases remain. |
| U06 | Partial | All packs have valid/invalid SHACL fixtures. Migration, stale data, ambiguity, and target-coverage tests remain incomplete. |
| U07 | Partial | Learning paths and runnable commands exist; not every lesson has a failure exercise and solution. |
| U08 | Partial | Eight editable teaching SVGs and text equivalents. Dedicated 390px compositions and per-asset exercises remain. |
| U09 | Partial | Five business queries and a fictional story; story's identity-reconciliation workflow is not implemented. |
| U10 | Partial | GO-inspired synthetic annotation pack; not a pinned GO extract, no valid external identifier/evidence-code/version exercise. |
| U11 | Partial | Compose and RDFTerm seed helper; live Neo4j parity, update/deletion semantics, timeout and access-control acceptance remain. |
| U12 | Partial | Fixture evaluator and citation-membership records. No entailment/source-span verification or contradiction assessment. |
| U13 | Partial | History pages, timeline table, three labeled fictional stories. Claim-level source coverage and a visual timeline remain. |
| U14 | Partial | ROI worksheet arithmetic and edge-case formulas; no executable scenario calculator. |
| U15 | Partial | Release workflow and changelog policy; no semantic migration/compatibility benchmark. |
| U16 | Partial | Contribution/reporting assets exist; fresh template-clone acceptance not demonstrated. |
| U17 | Partial | Ruff, mypy, task runner and pinned Compose version; service acceptance and environment locks remain. |
| U18 | Partial | Unicode-aware aliases, collision rejection and change records; no domain-pack review queue or reversible merge workflow. |
| U19 | Missing | No generated ontology reference or tested Chowlk workflow. |
| U20 | Scaffold | LinkML YAML loads; generator equivalence/cardinality coverage is not implemented. |
| U21 | Scaffold | Extraction policy dictionary and aliases; no extractor with evidence spans and SHACL-gated candidates. |
| U22 | Partial | Stdio listing/query/validation works; path restrictions and local SELECT policy tested. Execution resource isolation remains. |
| U23 | Missing | No extra store/model adapter with shared evaluation contract. |
| U24 | Partial | Twelve use-case rows and templates; not twelve detailed sponsor/data/deliverable/baseline case cards. |
| U25 | Partial | Seven consulting queries over a small synthetic pack; no conflicting/stale evidence workflow or decision packet. |
| U26 | Missing | No expert-reviewed quality/supply impact pack. |

## Visual review

Rasterized all 16 SVG exports with resvg and inspected a contact sheet plus
representative full-size images. The new illustrations provide a coherent
visual identity. Diagram correctness improved, but most graphics still use
simple cards and arrows. A wide 1400px canvas shrunk to 390px makes the 16px
body copy approximately 4.5px: mobile legibility is not accepted. Text equivalents
remain the readable fallback. YAML files are editorial briefs; Python is the
actual rendering source. The broad asset manifest is not a per-asset provenance
ledger. Three consulting diagrams remain missing: claim trace, identity
crosswalk, and quality impact.

## Writing audit assessment

Claude's supplied summary correctly identifies repeated qualifiers, generic
openings, and claims without measurements. Its “AI-generated” verdict and
numerical slop scores are subjective, not verified authorship or quality metrics.
Use sentence-level review: name the task, say what the code does, label fiction,
and attach evidence to outcomes. Do not mechanically delete necessary caveats
or replace vague promises with stronger unsupported promises.

The revised investment template asks for measurements. The stories distinguish
implemented pack behavior from imagined workflow outcomes. Code-of-conduct
language restores newcomer support. Prose checks suggest review locations but
do not fail CI for ordinary vocabulary.

## Verification and limits

Regression tests reproduced the path, query, evidence, parsing, CLI, evaluation,
link, and opt-in defects before their fixes. Automated checks cover the offline
core and mocked GraphRAG behavior. The real MCP stdio test covers initialization,
tool listing, valid validation/query calls, and outside-root rejection. All 22
named queries are compared to fixtures. LinkML SchemaView resolves the scaffold.
Local result: 112 tests passed with extras; 87 passed and three optional
modules skipped in the core-only environment. Package coverage: 85.25%.
Ruff, mypy, links, dependency consistency, and installed-environment dependency
audit passed. A wheel built and ran the manager query from a fresh environment
outside the checkout, against a separately copied examples directory. CI results must be checked for the
merged commit; local success alone is not a hosted acceptance claim.

No live Neo4j/LLM or real-client scientific validation is claimed. SHACL conformance
does not prove completeness, scientific truth, or legal/regulatory approval.
CodeRabbit independently found eight issues in the first pass, including query
question mismatches, blank-node stability, SVG line handling, links, and ROI
wording; each was checked against the source and addressed.

## Branch reconciliation

Before cleanup, every local and remote ref was saved in a verified Git bundle
outside this checkout. The visual and editorial branches are to be merged with
history preserved. The older Claude audit fixes have been superseded by the
current documentation; their original commit remains in the recovery bundle.
LangChain and langchain-community bump branches target packages no longer used.
The applicable OpenAI/Neo4j lower bounds and checkout/setup-python v7 changes
are included here (Actions pinned to resolved commit SHAs). Old dependency PRs
can therefore be closed as superseded after this commit passes hosted checks.
Do not move the published `v0.2.0` tag.

## Next implementation order

1. Replace experimental generated Cypher with named parameterized queries;
   prove read-only access and server cancellation against Neo4j.
2. Strengthen scientific/consulting fixtures: ambiguity, stale evidence,
   contradictions, source spans, and explicit review states.
3. Complete mobile visual compositions and the missing consulting diagrams;
   add exercises and per-asset provenance before further decorative artwork.
4. Expand the twelve consulting rows into engagement cards, then add the
   quality/supply pack with domain review.
5. Add locks, fresh-wheel acceptance, generated ontology reference, and the
   executable ROI scenarios. Keep new adapters demand-driven.

## Implementation update from `70f1679`

This table records the current branch evidence. “Partial” means the local
contract is implemented but the original external or domain-review acceptance
gate is still open.

| ID | Status | Current evidence | Remaining gate |
| --- | --- | --- | --- |
| U01 | Implemented / verified | Allowlisted parameterized templates are the normal Neo4j path; Enterprise profile verification proves a named read succeeds and a write is denied by the database role. | Repeat on an organisation-managed Enterprise cluster before production use. |
| U02 | Implemented / verified | `mcp_server.py` runs each query in a spawned disposable process; the 16-iteration benchmark reports zero workers before, during, and after repeated deadline terminations. | Tune limits for a deployment's workload. |
| U03 | Implemented / verified | Universal and Python 3.10/3.11/3.12 core/optional locks are generated and byte-checked by `scripts/regenerate_locks.py`; CI installs the matching versioned lock. | Regenerate when dependency inputs change. |
| U04 | Implemented / verified | Manifest field, version, ID, question/query consistency checks and all five-pack validation pass. | Add schema-version policy when a second manifest format is introduced. |
| U05 | Implemented / verified | Manager query now has dedicated unknown and ambiguous fixtures; `classify_single_answer` abstains rather than selecting a name, and the semantic tests cover both cases. | Add a domain-specific ambiguity policy if a real pack needs one. |
| U06 | Implemented / verified | Target-coverage validation and negative fixtures for missing fields, stale, ambiguous, and conflicting records pass. | Expand migration-specific invalid graph assertions. |
| U07 | Implemented / verified | `scripts/verify_lesson_commands.py` runs ten positive lesson, consulting, migration, ROI, extraction, and reference commands with the active interpreter; the workflow runs it in CI. | Repeat the clean-command check on each supported Python version when changing lesson dependencies. |
| U08 | Implemented / verified | `scripts/inspect_visuals.py` rendered and dimension-checked 29 desktop/mobile assets with Playwright; the 390×844 portrait montage was inspected for clipping, contrast, collisions, and label legibility. | Repeat visual inspection when artwork or font inputs change. |
| U09 | Implemented / verified | `identity-reconciliation.yaml` and `reconcile_business_ids.py` preserve IDs, decisions, reviewer/date/version, idempotence, collisions, and rollback. | Domain-owner review of the synthetic policy. |
| U10 | Partial / awaiting scientific review | External GO/ECO/NCBITaxon identifier shapes, version/retrieval metadata, taxon/evidence/review queries, negative fixtures, and a signed review register are present. | Named scientific reviewer must approve term mappings and evidence-code use. |
| U11 | Implemented / verified | Enterprise profile startup, health, role creation, named read, write denial, server cancellation, RDFLib parity, literal language, blank-node identity, and repeated import checks pass locally. | Repeat on an organisation-managed Enterprise cluster before production use. |
| U12 | Implemented / verified | `verify_source_spans` validates `source-id@start:end` offsets against the supplied source document; unit tests cover valid and out-of-range spans and `assess_answer` abstention. | Expand the reviewed evaluation set with domain-owned source documents. |
| U13 | Partial / awaiting editorial review | Four-lane history page, generated timeline, and ten-claim source register with authoritative URLs are present and machine-checked. | Named editor must review each claim and citation. |
| U14 | Implemented / verified | `roi.py`, `calculate_roi.py`, scenario fixture, zero-rate/no-payback and duplicate-benefit checks pass. | Replace hypothetical inputs with owner-approved measures for any real business case. |
| U15 | Implemented / verified | `docs/migrations/0.2-to-0.3.yaml` and `check_migration.py` demonstrate compatible/breaking paths and replacements; `v0.2.0` unchanged. | Add release-artifact comparison on the next tagged release. |
| U16 | Implemented / verified | Hosted repository API reports `is_template=true`, default branch `main`, and the issue form, citation metadata, and contribution/reporting files are present on the upgrade branch. | Recheck if repository settings are changed by an owner. |
| U17 | Implemented / verified locally | Enterprise Compose startup, health check, seed, read-only verifier, runtime parity/cancellation, and teardown pass; the profile is isolated from the Community volume. | Organisation-managed credentials and hosted service acceptance remain deployment-specific. |
| U18 | Implemented / verified | Review queue, explicit approve/reject states, reversible/idempotent application, and collision fixtures pass. | Domain-specific adjudication policy remains project-owned. |
| U19 | Implemented / verified | `docs/reference/chowlk-fixtures/claim-evidence.drawio` converts through the hosted Chowlk service; `scripts/verify_chowlk_conversion.py --live` returns no diagram errors and an empty semantic diff against the checked-in contract. | Review generated IRIs/cardinalities before adopting a diagram as canonical. |
| U20 | Implemented / verified | LinkML identifiers, required slots, enums, non-negative cardinalities, min/max ordering, multivalued rendering, and valid/invalid fixtures are covered by runtime tests; the clean locked optional environment passes `gen-json-schema --top-class Person --closed`. | Review conversion losses before using generated JSON Schema as a production contract. |
| U21 | Implemented / verified | Fixed-passage extraction returns exact spans and metadata; candidate RDF passes SHACL only as a reviewable diff. | Optional live-model runner and domain reviewer for extracted mappings. |
| U22 | Implemented / verified | MCP tests cover a 4,001-row payload larger than the pipe buffer, timeout boundary, malformed args, unknown query, symlink escape, response rejection, and worker cleanup; the 16-iteration benchmark shows no accumulation. | Tune limits for a deployment's workload. |
| U23 | Deferred | `docs/reference/adapter-decision.md` defines demand, owner, and shared-contract gates; no integration was added without a maintainer. | Named user demand and maintenance owner. |
| U24 | Partial / awaiting consultancy review | All 12 engagement cards include sponsor, users, decision, sources, slice, deliverable, measures, review, and boundaries; seven named operational templates are committed and linked. | Named life-science consultancy reviewer must test pilot scoping and assumptions. |
| U25 | Partial / awaiting domain review | Evidence-room pack has supported/unknown/conflicting/stale states, review queue, source dates/versions/spans, negative fixtures, and a reproducible decision packet. | Named therapeutic-area reviewer must assess the synthetic evidence policy. |
| U26 | Partial / awaiting domain review | Quality/supply pack covers products, sites, suppliers, materials, processes, methods, filings, changes, dependencies, stale and ambiguous states, with reproducible expected impact queries. | Named quality/supply expert must review the benchmark and expected-impact policy. |

### Follow-up verification from `feat/remaining-upgrade`

- `uv run --extra mcp --extra graphrag --with pytest --with pytest-cov pytest -q -ra --cov=src/ontology_starterkit --cov-fail-under=80`: 153 tests passed, two opt-in Neo4j tests skipped, 88.06% package coverage.
- `uv run python scripts/verify_lesson_commands.py`: ten documented positive commands passed from the checkout using the active interpreter.
- `uv run --extra graphrag python scripts/verify_neo4j_runtime.py`: named-query parity, language-tagged literal preservation, blank-node identity, repeated imports, server cancellation, and post-cancel heartbeat all passed against Neo4j 5.26.5 Community.
- `PATH=/tmp/ontokit-linkml-sk90N5/bin:$PATH python3 scripts/verify_linkml_generator.py`: LinkML 1.11.1 generated a closed JSON Schema that accepted `valid.yaml` and rejected `invalid.yaml`.
- `uv pip sync requirements/optional.lock` in a fresh `/tmp` environment installed all 151 locked packages and exposed `gen-json-schema` 1.11.1.
- `uv run --with build python -m build --wheel` plus `scripts/verify_wheel_install.py`: the wheel installed outside the checkout and ran the manager query.

### Gate closure evidence from this implementation pass

- `docker compose -f docker-compose.enterprise.yml --profile enterprise up -d --wait` followed by `scripts/verify_neo4j_service.py`: Enterprise startup, health, named read, database-enforced write denial, and server cancellation all passed; the profile was then torn down.
- `scripts/benchmark_mcp_isolation.py --iterations 16`: 16/16 bounded timeouts, zero workers before/at peak/after, and no accumulation.
- `scripts/regenerate_locks.py --write` followed by `scripts/regenerate_locks.py`: core and optional universal locks regenerated and byte-checked.
- `scripts/inspect_visuals.py --output-dir /tmp/ontokit-visual-review/renders`: 29 assets rendered with Playwright and checked at desktop and 390×844 mobile dimensions; the generated montages were inspected for clipping, contrast, collisions, and label legibility.
- `scripts/verify_source_spans` unit coverage: valid and out-of-range `source-id@start:end` spans produce the expected supported/insufficient outcomes.
- GitHub API verification: `is_template=true`, `default_branch=main`, and hosted issue-form/config, citation, contribution, and reporting files present.
- `scripts/verify_chowlk_conversion.py --live`: hosted Chowlk conversion returned no diagram errors and an empty semantic diff against the checked-in RDF contract.
- `scripts/check_review_register.py`: five external-review entries and ten sourced historical claims are present and machine-checked. Scientific, editorial, consultancy, and domain-expert sign-offs remain explicitly awaiting named reviewers; no approval is implied by the automated checks.

### Final verification at `8692365` — 2026-09-17

- Hosted governance, ontology validation, Python 3.10/3.11/3.12 tests, and locked core/optional environments all passed on GitHub Actions.
- Local verification after the final fixes: 157 tests passed, two opt-in Neo4j tests skipped, 87.64% package coverage; Ruff, mypy, lock freshness, lesson, MCP isolation, wheel, visual/link, review-register, and live Chowlk checks passed.
- The current checkout could not rerun Neo4j because the Docker daemon was unavailable. The earlier Enterprise/Community evidence above remains historical evidence from this branch, not a fresh run at this commit.
- U10, U13, U24, U25, and U26 remain awaiting named external reviewers; U23 remains deferred pending demand and a maintainer.
