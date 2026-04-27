from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import time

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


class MockResponse:
    def __init__(self, content: str):
        self.content = content


class MockLLM:
    def __init__(self, content: str):
        self.content = content

    def invoke(self, prompt: str):  # noqa: ARG002
        return MockResponse(self.content)


class MockGraph:
    def __init__(self, rows):
        self.rows = rows

    def query(self, query: str):  # noqa: ARG002
        return self.rows


class NonListGraph:
    def query(self, query: str):  # noqa: ARG002
        return {"not": "a-list"}


class SlowLLM:
    def invoke(self, prompt: str):  # noqa: ARG002
        time.sleep(0.05)
        return MockResponse("MATCH (n) RETURN n")


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


def test_validate_read_only_cypher_rejects_comment_or_semicolon():
    with pytest.raises(ValueError):
        graph_rag.validate_read_only_cypher("MATCH (n) RETURN n;")
    with pytest.raises(ValueError):
        graph_rag.validate_read_only_cypher("MATCH (n) RETURN n // injected")


def test_validate_read_only_cypher_with_limits_rejects_long_or_complex_query():
    long_query = "MATCH (n) RETURN n " + ("x" * 800)
    with pytest.raises(ValueError):
        graph_rag.validate_read_only_cypher_with_limits(long_query, max_query_length=100, max_match_clauses=3)

    complex_query = "MATCH (a) MATCH (b) MATCH (c) MATCH (d) RETURN a,b,c,d"
    with pytest.raises(ValueError):
        graph_rag.validate_read_only_cypher_with_limits(complex_query, max_query_length=700, max_match_clauses=3)


@pytest.mark.parametrize("query", [
    "CREATE (n:Person)",
    "MATCH (n) DELETE n",
    "MERGE (n:Person {name: 'Alice'})",
])
def test_validate_read_only_cypher_blocks_writes(query):
    with pytest.raises(ValueError):
        graph_rag.validate_read_only_cypher(query)


def test_generate_cypher_and_answer_question_with_mocks():
    settings = graph_rag.Settings(
        openai_api_key="test-key",
        neo4j_uri="bolt://localhost:7687",
        neo4j_username="neo4j",
        neo4j_password="test-password",
    )
    guards = graph_rag.RuntimeGuards(max_llm_calls=4, max_graph_queries=2)
    run_id = "test-run"

    cypher_llm = MockLLM("MATCH (n) RETURN n LIMIT 1")
    qa_llm = MockLLM("Alice works on Alpha Project.")
    graph = MockGraph(rows=[{"name": "Alice"}])

    cypher = graph_rag.generate_cypher(
        question="Who works on Alpha Project?",
        schema="(Person)-[:WORKS_ON]->(Project)",
        llm=cypher_llm,
        settings=settings,
        guards=guards,
        run_id=run_id,
    )
    assert cypher == "MATCH (n) RETURN n LIMIT 1"

    rows = graph_rag.run_graph_query(
        graph=graph,
        query=cypher,
        timeout_seconds=5,
        guards=guards,
        run_id=run_id,
    )
    assert rows == [{"name": "Alice"}]

    answer = graph_rag.answer_question(
        question="Who works on Alpha Project?",
        rows=rows,
        llm=qa_llm,
        settings=settings,
        guards=guards,
        run_id=run_id,
    )
    assert "Alice" in answer


def test_runtime_guards_enforce_call_limits():
    settings = graph_rag.Settings(
        openai_api_key="test-key",
        neo4j_uri="bolt://localhost:7687",
        neo4j_username="neo4j",
        neo4j_password="test-password",
    )
    guards = graph_rag.RuntimeGuards(max_llm_calls=1, max_graph_queries=1)
    run_id = "guard-test"
    llm = MockLLM("MATCH (n) RETURN n LIMIT 1")

    graph_rag.generate_cypher(
        question="Q1",
        schema="schema",
        llm=llm,
        settings=settings,
        guards=guards,
        run_id=run_id,
    )
    with pytest.raises(ValueError):
        graph_rag.generate_cypher(
            question="Q2",
            schema="schema",
            llm=llm,
            settings=settings,
            guards=guards,
            run_id=run_id,
        )


def test_runtime_guards_enforce_graph_query_limits():
    guards = graph_rag.RuntimeGuards(max_llm_calls=2, max_graph_queries=1)
    guards.consume_graph_query()
    with pytest.raises(ValueError):
        guards.consume_graph_query()


def test_invoke_llm_with_timeout_raises():
    guards = graph_rag.RuntimeGuards(max_llm_calls=1, max_graph_queries=1)
    with pytest.raises(TimeoutError):
        graph_rag.invoke_llm_with_timeout(
            llm=SlowLLM(),
            prompt="test",
            timeout_seconds=0,
            guards=guards,
            run_id="timeout-test",
        )


def test_run_graph_query_requires_list():
    guards = graph_rag.RuntimeGuards(max_llm_calls=2, max_graph_queries=2)
    with pytest.raises(TypeError):
        graph_rag.run_graph_query(
            graph=NonListGraph(),
            query="MATCH (n) RETURN n",
            timeout_seconds=1,
            guards=guards,
            run_id="not-list",
        )


def test_parse_args_with_cli(monkeypatch):
    monkeypatch.setattr("sys.argv", ["graph_rag.py", "--query", "Who works on Alpha?"])
    args = graph_rag.parse_args()
    assert args.query == "Who works on Alpha?"


def test_main_success_path(monkeypatch):
    class Args:
        query = "Who works on Alpha?"

    settings = graph_rag.Settings(
        openai_api_key="test-key",
        neo4j_uri="bolt://localhost:7687",
        neo4j_username="neo4j",
        neo4j_password="test-password",
    )

    monkeypatch.setattr(graph_rag, "parse_args", lambda: Args())
    monkeypatch.setattr(graph_rag, "load_settings", lambda: settings)
    monkeypatch.setattr(graph_rag, "setup_graph", lambda s: object())  # noqa: ARG005
    monkeypatch.setattr(graph_rag, "get_graph_schema", lambda g: "schema")  # noqa: ARG005
    monkeypatch.setattr(graph_rag, "build_llm", lambda model, api_key, timeout_seconds: object())  # noqa: ARG005
    monkeypatch.setattr(graph_rag, "generate_cypher", lambda **kwargs: "MATCH (n) RETURN n LIMIT 1")
    monkeypatch.setattr(graph_rag, "run_graph_query", lambda **kwargs: [{"name": "Alice"}])
    monkeypatch.setattr(graph_rag, "answer_question", lambda **kwargs: "Alice")

    assert graph_rag.main() == 0


def test_main_value_error_path(monkeypatch):
    class Args:
        query = "Q"

    monkeypatch.setattr(graph_rag, "parse_args", lambda: Args())
    monkeypatch.setattr(graph_rag, "load_settings", lambda: (_ for _ in ()).throw(ValueError("bad config")))

    assert graph_rag.main() == 1
