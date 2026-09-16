import pytest

from ontology_starterkit.linkml import build_linkml_schema


def test_linkml_scaffold_is_deterministic_and_contains_classes():
    schema = build_linkml_schema("hello", {"Person": ["name", "name"], "Team": ["name"]})
    assert "classes:" in schema
    assert "Person:" in schema
    assert schema.count("- name") == 2


def test_linkml_scaffold_rejects_invalid_identifiers():
    with pytest.raises(ValueError, match="class identifier"):
        build_linkml_schema("hello", {"not a class": ["name"]})


def test_linkml_supports_reviewed_cardinality_enum_and_identifier():
    schema = build_linkml_schema(
        "hello", {"Person": ["id", "status"]},
        slot_specs={"id": {"identifier": True, "required": True}, "status": {"enum": ["active", "retired"]}},
    )
    assert "identifier: true" in schema
    assert "StatusEnum" in schema
    assert "active" in schema
