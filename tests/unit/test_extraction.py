from ontology_starterkit.extraction import extraction_contract, normalize_identifier, resolve_aliases


def test_normalize_identifier_is_stable():
    assert normalize_identifier("  TNF-α / 1 ") == "tnf 1"


def test_resolve_aliases_applies_only_reviewed_values():
    records = [{"asset": "Project Alpha", "owner": "Unreviewed"}]
    assert resolve_aliases(records, {"project alpha": "ex:Alpha"}) == [
        {"asset": "ex:Alpha", "owner": "Unreviewed"}
    ]


def test_extraction_contract_requires_provenance_and_abstention():
    contract = extraction_contract([" Claim ", "Claim", "Source"])
    assert contract["terms"] == ("Claim", "Source")
    assert contract["require_source_span"] is True
    assert contract["abstain_on_ambiguity"] is True

