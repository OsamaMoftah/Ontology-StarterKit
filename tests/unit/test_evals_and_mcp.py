from pathlib import Path

from ontology_starterkit.evals import evaluate_query
from ontology_starterkit.mcp_server import list_pack_tools, run_query_tool, validate_pack_tool
from ontology_starterkit.packs import load_pack


ROOT = Path(__file__).resolve().parents[2]


def test_evaluate_query_matches_fixture():
    result = evaluate_query(load_pack(ROOT / "examples/hello-ontology"), "manager")
    assert result["passed"] is True


def test_mcp_adapter_exposes_declared_queries_only():
    tools = list_pack_tools(ROOT / "examples")
    assert {item["pack"] for item in tools} >= {"hello-ontology", "consulting-evidence-room"}
    assert all(item["query"] for item in tools)


def test_mcp_pure_tools_are_json_safe():
    path = ROOT / "examples/hello-ontology"
    assert validate_pack_tool(path)["conforms"] is True
    assert run_query_tool(path, "manager")["rows"]

