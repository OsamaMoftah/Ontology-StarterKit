default:
    @just --list

test:
    python -m pytest -q

lint:
    ruff check .

typecheck:
    mypy src/ontology_starterkit

validate:
    python -m ontology_starterkit.cli packs
    python -m ontology_starterkit.cli validate examples/hello-ontology
    python -m ontology_starterkit.cli validate examples/business-projects
    python -m ontology_starterkit.cli validate examples/life-science-annotations
    python -m ontology_starterkit.cli validate examples/consulting-evidence-room

diagrams:
    python scripts/render_diagrams.py

services-up:
    docker compose --profile services up -d --wait

services-ready: services-up
    docker compose --profile services ps

services-seed: services-up
    python scripts/seed_neo4j.py examples/hello-ontology
