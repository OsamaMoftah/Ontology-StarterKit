from pathlib import Path

import pytest

from ontology_starterkit.packs import discover_packs
from ontology_starterkit.evals import evaluate_query
from ontology_starterkit.validation import run_named_query, validate_pack


ROOT = Path(__file__).resolve().parents[2]


def test_all_domain_packs_have_valid_and_invalid_fixtures():
    packs = discover_packs(ROOT / "examples")
    assert {"business-projects", "life-science-annotations", "consulting-evidence-room", "quality-supply-impact"} <= set(packs)
    for pack in packs.values():
        assert validate_pack(pack).conforms is True
        assert pack.manifest.get("invalid")
        for path in pack.manifest["invalid"]:
            assert validate_pack(pack, data_path=path).conforms is False


def test_domain_packs_have_a_real_competency_question_set():
    packs = discover_packs(ROOT / "examples")
    assert len(packs["hello-ontology"].manifest["queries"]) >= 5
    assert len(packs["business-projects"].manifest["queries"]) >= 5
    assert len(packs["life-science-annotations"].manifest["queries"]) >= 5
    assert len(packs["consulting-evidence-room"].manifest["queries"]) >= 7
    assert len(packs["quality-supply-impact"].manifest["queries"]) >= 4


@pytest.mark.parametrize("pack_id,query_id", [
    ("business-projects", "owner"),
    ("life-science-annotations", "evidence"),
    ("consulting-evidence-room", "unsupported"),
    ("quality-supply-impact", "impact"),
])
def test_domain_queries_return_rows(pack_id, query_id):
    pack = discover_packs(ROOT / "examples")[pack_id]
    rows = run_named_query(pack, query_id)
    assert rows
    assert evaluate_query(pack, query_id)["passed"] is True


@pytest.mark.parametrize("pack,query_id", [
    (pack, query_id)
    for pack in discover_packs(ROOT / "examples").values()
    for query_id in pack.manifest["queries"]
], ids=lambda item: item.pack_id if hasattr(item, "pack_id") else item)
def test_every_named_query_matches_its_fixture(pack, query_id):
    assert evaluate_query(pack, query_id)["passed"] is True
