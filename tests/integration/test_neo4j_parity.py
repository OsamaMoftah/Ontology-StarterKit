import os

import pytest


pytestmark = pytest.mark.integration


def test_live_neo4j_parity_term_fidelity_and_server_cancellation():
    if os.getenv("ONTOLOGY_RUN_NEO4J") != "1":
        pytest.skip("set ONTOLOGY_RUN_NEO4J=1 after starting the documented Compose service")
    from scripts.verify_neo4j_runtime import verify

    result = verify(
        os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687"),
        os.getenv("NEO4J_USERNAME", "neo4j"),
        os.getenv("NEO4J_PASSWORD", "starterkit-local-only"),
    )
    assert result == {
        "query_parity": True,
        "expected_rows": 1,
        "actual_rows": 1,
        "literal_language_preserved": True,
        "blank_node_identity_preserved": True,
        "repeated_imports_idempotent": True,
        "server_cancelled": True,
        "post_cancel_heartbeat": True,
    }
