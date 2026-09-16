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
    for pack in examples/*; do python -m ontology_starterkit.cli validate "$pack"; done

diagrams:
    python scripts/render_diagrams.py

visuals: diagrams
    python scripts/render_infographics.py
    python scripts/render_mobile_infographics.py

services-up:
    docker compose --profile services up -d --wait

services-ready: services-up
    docker compose --profile services ps

services-seed: services-up
    python scripts/seed_neo4j.py examples/hello-ontology

services-verify: services-seed
    ONTOLOGY_RUN_NEO4J=1 python scripts/verify_neo4j_service.py

services-down:
    docker compose --profile services down
