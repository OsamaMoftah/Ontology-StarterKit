# Ontology StarterKit

> The practical starter repository for ontology-first AI products.

Ontology StarterKit is a documentation-first, engineering-backed repository for teams that want to use ontologies, knowledge graphs, and GraphRAG in real AI products without requiring deep semantic web expertise.

It is intentionally opinionated:

- Start with business value, not ontology purity.
- Use modern AI tooling such as LangChain and Neo4j where it speeds adoption.
- Treat governance, validation, and reproducibility as first-class concerns.
- Clearly distinguish between what is implemented today and what is planned next.

## What Is Implemented Today

### For AI Engineers

- [KG-RAG example](src/integrations/langchain/kg-rag/README.md): a safer LangChain + Neo4j example with environment validation, query guardrails, and tests.
- [Sample ontology assets](src/ontology/README.md): minimal SHACL shapes and RDF data so validation workflows are real.

### For Product Managers

- [ROI calculator](docs/for-product-managers/roi-calculator/README.md): practical ROI, NPV, and payback templates.
- [Decision framework](docs/for-product-managers/decision-framework.md): how to choose between RDF, property graphs, and hybrid vector-graph systems.
- [Investment one-pager](docs/for-product-managers/investment-one-pager.md): an executive-ready summary template.

### For Founders and Small Teams

- [30-day sprint guide](docs/for-startups/30-day-sprint.md): a realistic startup execution path from problem framing to launch.

### Governance and Release

- [Schema change review policy](docs/governance/schema-change-review.md): review expectations and compatibility guidance for ontology changes.
- [Release process](docs/governance/release-process.md): release checklist, versioning rules, and note quality standards.

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
pip install -r src/integrations/langchain/kg-rag/requirements.txt
pip install pytest
cp .env.example .env
```

### 3. Run tests

```bash
pytest
```

### 4. Run ontology validation locally

```bash
pip install pyshacl rdflib
pyshacl -s src/ontology/shapes.ttl -m -i rdfs -a -f human src/ontology/data.ttl
```

### 5. Run the KG-RAG example

```bash
python3 src/integrations/langchain/kg-rag/graph_rag.py --query "Who manages the team that works on the Alpha Project?"
```

See the [documentation index](docs/README.md) for a full list of every doc in this repository, grouped by audience.

## Repository Structure

```text
Ontology-StarterKit/
├── .github/workflows/            # CI workflows for tests and ontology validation
├── docs/
│   ├── for-product-managers/     # ROI and architecture decision assets
│   └── for-startups/             # Startup-oriented execution guides
├── src/
│   ├── integrations/langchain/   # LLM and graph integration examples
│   └── ontology/                 # Sample ontology data and SHACL shapes
└── tests/                        # Smoke tests for executable examples
```

## Project Positioning

This repository is suitable as a public, documentation-first starter kit. It is not intended to represent a complete framework or enterprise platform. Every implemented example in the repository should be runnable, reviewed, and supported by accurate documentation.

## Roadmap

Planned next additions include:

- Architecture and scalability patterns
- More integration examples beyond LangChain
- Case studies with measurable outcomes
- Expanded governance templates

## License

Released under the [MIT License](LICENSE).
