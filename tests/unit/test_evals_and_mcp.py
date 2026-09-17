from pathlib import Path
import multiprocessing
import shutil
import time
import pytest

from ontology_starterkit.evals import evaluate_query
from ontology_starterkit.mcp_server import list_pack_tools, run_query_tool, validate_pack_tool
from ontology_starterkit.packs import PackError, load_pack
from ontology_starterkit.validation import validate_named_query


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
    result = run_query_tool(path, "manager")
    assert result["rows"]
    assert result["limits"]["worker"] == "process"
    assert not multiprocessing.active_children()


def test_mcp_drains_a_genuinely_large_result_before_reaping_worker(tmp_path):
    source = ROOT / "examples/hello-ontology"
    path = tmp_path / "large-ontology"
    shutil.copytree(source, path)
    rows = [
        f'ex:Person{i} a ex:Person ; ex:name "Person {i:05d} with a deliberately large name" .'
        for i in range(4_000)
    ]
    (path / "data/valid.ttl").write_text(
        "@prefix ex: <https://ontology-starterkit.dev/hello/> .\n"
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
        'ex:Maya a ex:Person ; ex:name "Maya Chen"^^xsd:string ; ex:manages ex:Aurora .\n'
        'ex:Aurora a ex:Team ; ex:name "Team Aurora"^^xsd:string ; ex:worksOn ex:Alpha .\n'
        'ex:Alpha a ex:Project ; ex:name "Alpha Project"^^xsd:string .\n'
        + "\n".join(rows)
        + "\n",
        encoding="utf-8",
    )

    result = run_query_tool(path, "people", max_rows=10_000, max_bytes=10_000_000, timeout_seconds=10)

    assert len(result["rows"]) == 4_001
    assert len(str(result["rows"]).encode("utf-8")) > 64_000
    assert not multiprocessing.active_children()


def test_mcp_reaps_worker_after_response_rejection():
    path = ROOT / "examples/hello-ontology"
    with pytest.raises(PackError, match="exceeds 1 bytes"):
        run_query_tool(path, "manager", max_bytes=1)
    assert not multiprocessing.active_children()


def test_mcp_query_limits_and_arguments_are_enforced():
    import pytest

    path = ROOT / "examples/hello-ontology"
    with pytest.raises(PackError, match="integer between"):
        run_query_tool(path, "manager", max_rows=0)
    with pytest.raises(PackError, match="exceeds 1 bytes"):
        run_query_tool(path, "manager", max_bytes=1)
    with pytest.raises(PackError, match="unknown named query"):
        run_query_tool(path, "does-not-exist")
    assert not multiprocessing.active_children()
    with pytest.raises(PackError, match="deadline"):
        run_query_tool(path, "manager", timeout_seconds=0.000001)


def test_mcp_tools_reject_pack_paths_outside_root(tmp_path):
    import pytest
    path = ROOT / "examples/hello-ontology"
    with pytest.raises(PackError, match="examples root"):
        validate_pack_tool(path, examples_root=tmp_path)


def test_mcp_timeout_terminates_the_worker_process():
    path = ROOT / "examples/hello-ontology"
    started = time.monotonic()
    with pytest.raises(PackError, match="deadline"):
        run_query_tool(path, "manager", timeout_seconds=0.02, _worker_delay_seconds=0.25)
    assert time.monotonic() - started < 1.5
    assert not multiprocessing.active_children()


def test_mcp_repeated_timeouts_do_not_accumulate_workers():
    path = ROOT / "examples/hello-ontology"
    for _ in range(8):
        with pytest.raises(PackError, match="deadline"):
            run_query_tool(path, "manager", timeout_seconds=0.01, _worker_delay_seconds=0.1)
    assert not multiprocessing.active_children()


def test_named_query_rejects_remote_service_operation():
    import pytest
    with pytest.raises(PackError, match="local read"):
        validate_named_query("SELECT * WHERE { SERVICE <https://remote.invalid> { ?s ?p ?o } }")
