from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "integrations" / "langchain" / "kg-rag" / "graph_rag.py"
SPEC = spec_from_file_location("graph_rag_module", MODULE_PATH)
graph_rag = module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(graph_rag)


class CallableSchemaGraph:
    def get_schema(self):
        return "CALLABLE_SCHEMA"


class PropertySchemaGraph:
    schema = "PROPERTY_SCHEMA"


@pytest.fixture
def valid_env():
    return {
        "OPENAI_API_KEY": "test-key",
        "NEO4J_PASSWORD": "test-password",
    }


def test_load_settings_requires_required_values():
    with pytest.raises(ValueError):
        graph_rag.load_settings({})


def test_load_settings_uses_defaults(valid_env):
    settings = graph_rag.load_settings(valid_env)
    assert settings.neo4j_uri == "bolt://localhost:7687"
    assert settings.neo4j_username == "neo4j"


def test_get_graph_schema_supports_callable_property():
    assert graph_rag.get_graph_schema(CallableSchemaGraph()) == "CALLABLE_SCHEMA"
    assert graph_rag.get_graph_schema(PropertySchemaGraph()) == "PROPERTY_SCHEMA"


def test_validate_read_only_cypher_allows_match():
    query = "MATCH (n) RETURN n LIMIT 5"
    assert graph_rag.validate_read_only_cypher(query) == query


@pytest.mark.parametrize("query", [
    "CREATE (n:Person)",
    "MATCH (n) DELETE n",
    "MERGE (n:Person {name: 'Alice'})",
])
def test_validate_read_only_cypher_blocks_writes(query):
    with pytest.raises(ValueError):
        graph_rag.validate_read_only_cypher(query)
