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

