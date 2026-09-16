# Ontology StarterKit

![Ontology workshop hero](media/source/illustrations/ontology-workshop-hero.png)

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](pyproject.toml) [![License](https://img.shields.io/badge/license-MIT-green)](LICENSE) [![Offline packs](https://img.shields.io/badge/core-offline--first-purple)](docs/learn/README.md)

> Build ontology-backed AI products. Start here.

This starter repo shows how to add ontologies, knowledge graphs, and GraphRAG to AI products without prior semantic-web expertise.

Start with the [10-minute offline path](docs/learn/README.md), browse the [visual gallery](media/gallery.md), run a [business ownership pack](examples/business-projects/README.md), a [life-science annotation pack](examples/life-science-annotations/README.md), or the [life-sciences consulting path](docs/consulting/README.md). Neo4j and LLM integrations are optional extensions.

The repo is opinionated:

- Start with business value, not ontology purity.
- Use modern AI tooling such as LangChain and Neo4j where it speeds adoption.
- Governance, validation, and reproducibility are built into the CI.
- Clearly distinguish between what is implemented today and what is planned next.

## What Is Implemented Today

### For AI Engineers

- [KG-RAG example](src/integrations/langchain/kg-rag/README.md): a LangChain + Neo4j example with read-only Cypher validation, query guardrails, and tests.
- [Sample ontology assets](src/ontology/README.md): minimal SHACL shapes and RDF data so validation workflows are real.
- [Example packs](examples/hello-ontology/README.md): model, data, shapes, questions, expected outputs and evidence metadata.

### For Product Managers

- [ROI calculator](docs/for-product-managers/roi-calculator/README.md): ROI, NPV, and payback-period templates with fillable formulas.
- [Decision framework](docs/for-product-managers/decision-framework.md): how to choose between RDF, property graphs, and hybrid vector-graph systems.
- [Investment one-pager](docs/for-product-managers/investment-one-pager.md): a one-page template for pitching the investment.

### For Founders and Small Teams

- [30-day sprint guide](docs/for-startups/30-day-sprint.md): a 30-day plan from problem framing to launch.

### Governance and Release

- [Schema change review policy](docs/governance/schema-change-review.md): review expectations and compatibility guidance for ontology changes.
- [Release process](docs/governance/release-process.md): release checklist, versioning rules, and note quality standards.

### Learn and Apply

- [Learning path](docs/learn/README.md)
- [History of ontology in business, life sciences and AI](docs/history/README.md)
- [Consulting use cases](docs/consulting/README.md)
- [Visual assets](assets/README.md)
- [Infographic lessons](docs/learn/infographics.md)
- [Fictional workshop stories](docs/stories/README.md)

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/OsamaMoftah/Ontology-StarterKit.git
cd Ontology-StarterKit
```

### 2. Create a local environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
cp .env.example .env
```

### 3. Run tests

```bash
pytest
```

The core test run skips GraphRAG-only modules when their optional dependencies
are absent. To exercise that adapter too, install `pip install -e '.[dev,graphrag]'`.

### 4. Run ontology validation locally

```bash
ontokit validate examples/hello-ontology
```

### 5. Run the offline competency query

```bash
ontokit packs
python - <<'PY'
from ontology_starterkit.packs import load_pack
from ontology_starterkit.validation import run_named_query
pack = load_pack('examples/hello-ontology')
print(run_named_query(pack, 'manager'))
PY
```

### 6. Run the optional KG-RAG example

```bash
python3 src/integrations/langchain/kg-rag/graph_rag.py --query "Who manages the team that works on the Alpha Project?"
```

For a local Neo4j only, opt in to the pinned Compose service with
`docker compose --profile services up -d`. Keep the default password local and
replace it before any shared environment.

See the [documentation index](docs/README.md) for the full learning, consulting and engineering paths.

## Repository Structure

```text
Ontology-StarterKit/
├── .github/workflows/            # CI workflows for tests and ontology validation
├── docs/                         # Learn, history, consulting, PM and governance
├── examples/                     # Self-contained domain packs
├── media/                        # Manifest and generated diagrams
├── scripts/                      # Deterministic visual/build helpers
├── src/
│   ├── integrations/langchain/   # LLM and graph integration examples
│   └── ontology/                 # Sample ontology data and SHACL shapes
└── tests/                        # Smoke tests for executable examples
```

## Project Positioning

This is a starter kit, not a framework. The offline examples run in the test suite; the Neo4j and LLM examples need their services and credentials.

## Current boundary

The repository now ships deterministic teaching and consulting visuals, four
multi-question packs, evidence-shaped answer helpers, and bounded optional
adapters. Production deployments still need a service-specific security review,
client-owned terminology licenses, domain reviewers, and live Neo4j/LLM
acceptance tests.

## License

Released under the [MIT License](LICENSE).
