import pytest

from ontology_starterkit.entity_resolution import apply_decisions, approve_decision, review_alias_candidates, rollback_decisions


def test_aliases_need_review_and_approved_mappings_are_reversible():
    records = [{"id": "r1", "name": "Acme Ltd"}, {"id": "r2", "name": "Acme"}]
    decisions = review_alias_candidates(records, {"Acme Ltd": "org:acme"}, field="name", mapping_version="v1")
    assert decisions[0].status == "queued"
    assert decisions[1].status == "unmatched"
    approved = approve_decision(decisions[0], "reviewer@example.test", approved_on="2026-09-16")
    mapped = apply_decisions(records, [approved])
    assert mapped == [{"id": "r1", "name": "org:acme"}, records[1]]
    assert rollback_decisions(mapped, [approved]) == records
    assert apply_decisions(mapped, [approved]) == mapped


def test_collisions_are_ambiguous_and_cannot_be_approved():
    records = [{"id": "r1", "name": "Acme"}]
    decision = review_alias_candidates(records, {"Acme": "org:a", " acme ": "org:b"}, field="name", mapping_version="v1")[0]
    assert decision.status == "ambiguous"
    with pytest.raises(ValueError):
        approve_decision(decision, "reviewer")
