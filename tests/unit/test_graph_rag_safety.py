from pathlib import Path
import importlib.util
import time

import pytest


MODULE_PATH = Path(__file__).resolve().parents[2] / "src/integrations/langchain/kg-rag/graph_rag.py"
SPEC = importlib.util.spec_from_file_location("graph_rag_safety", MODULE_PATH)
module = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(module)


def test_cypher_rejects_procedures_and_accepts_domain_identifiers():
    with pytest.raises(ValueError, match="procedure"):
        module.validate_read_only_cypher("CALL apoc.cypher.doIt($statement, {}) YIELD value RETURN value")
    assert module.validate_read_only_cypher("MATCH (n:Dataset) RETURN n.createdAt LIMIT 5")


def test_cypher_rejects_unbounded_variable_length_paths_and_cartesian_products():
    with pytest.raises(ValueError, match="path"):
        module.validate_read_only_cypher("MATCH p=(a)-[*]->(b) RETURN p LIMIT 5")
    with pytest.raises(ValueError, match="Cartesian"):
        module.validate_read_only_cypher("MATCH (a),(b) RETURN a,b LIMIT 5")


def test_empty_env_mapping_does_not_read_process_environment(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "ambient")
    monkeypatch.setenv("NEO4J_PASSWORD", "ambient")
    with pytest.raises(ValueError, match="OPENAI_API_KEY"):
        module.load_settings({})


def test_invalid_runtime_values_are_rejected():
    env = {"OPENAI_API_KEY": "key", "NEO4J_PASSWORD": "password", "GRAPH_TIMEOUT_SECONDS": "0"}
    with pytest.raises(ValueError, match="positive"):
        module.load_settings(env)


def test_llm_timeout_returns_without_waiting_for_worker():
    class Slow:
        def invoke(self, prompt):
            time.sleep(0.2)
            return prompt

    start = time.monotonic()
    with pytest.raises(TimeoutError):
        module.invoke_llm_with_timeout(Slow(), "x", 0.01, module.RuntimeGuards(1, 1), "run")
    assert time.monotonic() - start < 0.1
