import os

import pytest


pytestmark = pytest.mark.integration


def test_real_neo4j_read_only_and_server_cancellation():
    if os.getenv("ONTOLOGY_RUN_NEO4J") != "1":
        pytest.skip("set ONTOLOGY_RUN_NEO4J=1 after starting the documented Compose service")
    from scripts.verify_neo4j_service import verify

    result = verify(
        os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687"),
        os.getenv("NEO4J_USERNAME", "neo4j"),
        os.getenv("NEO4J_PASSWORD", "starterkit-local-only"),
    )
    assert result == {"named_query": True, "write_denied": True, "server_cancelled": True}
