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

lessons:
    python scripts/verify_lesson_commands.py

locks:
    python scripts/regenerate_locks.py

review-register:
    python scripts/check_review_register.py

chowlk:
    python scripts/verify_chowlk_conversion.py

chowlk-live:
    python scripts/verify_chowlk_conversion.py --live

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

services-runtime: services-seed
    python scripts/verify_neo4j_runtime.py

services-access-control: services-seed
    ONTOLOGY_RUN_NEO4J=1 python scripts/verify_neo4j_service.py

enterprise-up:
    docker compose -f docker-compose.enterprise.yml --profile enterprise up -d --wait

enterprise-verify: enterprise-up
    NEO4J_URI=bolt://127.0.0.1:7688 NEO4J_PASSWORD=starterkit-enterprise-local python scripts/verify_neo4j_service.py

enterprise-down:
    docker compose -f docker-compose.enterprise.yml --profile enterprise down

services-down:
    docker compose --profile services down
