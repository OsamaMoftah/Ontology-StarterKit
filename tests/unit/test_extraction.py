import pytest

from ontology_starterkit.extraction import extraction_contract, normalize_identifier, resolve_aliases, resolve_aliases_with_audit


def test_normalize_identifier_is_stable():
    assert normalize_identifier("  TNF-α / 1 ") == "tnf α 1"
    assert normalize_identifier("TNF-α") != normalize_identifier("TNF-β")


def test_resolve_aliases_applies_only_reviewed_values():
    records = [{"asset": "Project Alpha", "owner": "Unreviewed"}]
    assert resolve_aliases(records, {"project alpha": "ex:Alpha"}) == [
        {"asset": "ex:Alpha", "owner": "Unreviewed"}
    ]


def test_resolve_aliases_can_limit_fields_and_reject_collisions():
    records = [{"asset": "TNF-α", "owner": "TNF-β"}]
    assert resolve_aliases(records, {"TNF-α": "ex:Alpha", "TNF-β": "ex:Beta"}, fields={"asset"}) == [
        {"asset": "ex:Alpha", "owner": "TNF-β"}
    ]
    with pytest.raises(ValueError, match="alias collision"):
        resolve_aliases(records, {"Project-Alpha": "ex:One", "Project Alpha": "ex:Two"})


def test_resolve_aliases_with_audit_records_provenance():
    audited = resolve_aliases_with_audit([{"asset": "Project Alpha"}], {"Project Alpha": "ex:Alpha"})
    assert audited[0]["record"]["asset"] == "ex:Alpha"
    assert audited[0]["changes"][0]["original"] == "Project Alpha"


def test_extraction_contract_requires_provenance_and_abstention():
    contract = extraction_contract([" Claim ", "Claim", "Source"])
    assert contract["terms"] == ("Claim", "Source")
    assert contract["require_source_span"] is True
    assert contract["abstain_on_ambiguity"] is True
