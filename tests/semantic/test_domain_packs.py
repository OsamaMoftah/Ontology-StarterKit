from pathlib import Path

import pytest

from ontology_starterkit.packs import discover_packs
from ontology_starterkit.evals import evaluate_query
from ontology_starterkit.validation import run_named_query, validate_pack


ROOT = Path(__file__).resolve().parents[2]


def test_all_domain_packs_have_valid_and_invalid_fixtures():
    packs = discover_packs(ROOT / "examples")
    assert {"business-projects", "life-science-annotations", "consulting-evidence-room"} <= set(packs)
    for pack in packs.values():
        assert validate_pack(pack).conforms is True
        assert pack.manifest.get("invalid")
        for path in pack.manifest["invalid"]:
            assert validate_pack(pack, data_path=path).conforms is False


@pytest.mark.parametrize("pack_id,query_id", [
    ("business-projects", "owner"),
    ("life-science-annotations", "evidence"),
    ("consulting-evidence-room", "unsupported"),
])
def test_domain_queries_return_rows(pack_id, query_id):
    pack = discover_packs(ROOT / "examples")[pack_id]
    rows = run_named_query(pack, query_id)
    assert rows
    assert evaluate_query(pack, query_id)["passed"] is True
