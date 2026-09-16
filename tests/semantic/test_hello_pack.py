from pathlib import Path

import pytest

from ontology_starterkit.packs import PackError
from ontology_starterkit.packs import load_pack
from ontology_starterkit.validation import run_named_query, validate_pack


ROOT = Path(__file__).resolve().parents[2]
PACK = load_pack(ROOT / "examples/hello-ontology")


def test_hello_valid_fixture_conforms_and_manager_query_is_exact():
    report = validate_pack(PACK, data_path="data/valid.ttl")
    assert report.conforms is True
    rows = run_named_query(PACK, "manager", data_path="data/valid.ttl")
    assert rows == [{"person": "https://ontology-starterkit.dev/hello/Maya", "personName": "Maya Chen"}]


def test_hello_invalid_fixtures_fail_for_intended_constraints():
    assert validate_pack(PACK, data_path="data/invalid/missing-name.ttl").conforms is False
    assert validate_pack(PACK, data_path="data/invalid/bad-relation.ttl").conforms is False


def test_hello_empty_graph_is_rejected_by_pack_target_check():
    empty = ROOT / "examples" / "hello-ontology" / "data" / "empty-temp.ttl"
    empty.write_text("@prefix ex: <https://ontology-starterkit.dev/hello/> .\n")
    try:
        report = validate_pack(PACK, data_path=str(empty))
        assert report.conforms is False
        assert "empty" in report.messages[0].lower()
    finally:
        empty.unlink()


def test_named_query_rejects_untrusted_parameters():
    with pytest.raises(PackError, match="parameters"):
        run_named_query(PACK, "manager", parameters={"name": "Maya"})
