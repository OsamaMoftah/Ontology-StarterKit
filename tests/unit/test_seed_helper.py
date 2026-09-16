from scripts.seed_neo4j import _local_uri


def test_seed_helper_accepts_only_local_uris():
    assert _local_uri("bolt://localhost:7687") is True
    assert _local_uri("bolt://127.0.0.1:7687") is True
    assert _local_uri("neo4j+s://customer.example") is False

