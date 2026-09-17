import pytest
import yaml

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


def test_linkml_renders_multivalued_cardinality():
    schema = build_linkml_schema(
        "hello", {"Person": ["aliases"]},
        slot_specs={"aliases": {"minimum_cardinality": 1, "maximum_cardinality": 3}},
    )
    assert "multivalued: true" in schema
    assert "minimum_cardinality: 1" in schema
    assert "maximum_cardinality: 3" in schema


def test_linkml_keeps_zero_to_one_cardinality_single_valued():
    schema = build_linkml_schema(
        "hello", {"Person": ["alias"]},
        slot_specs={"alias": {"minimum_cardinality": 0, "maximum_cardinality": 1}},
    )
    alias = yaml.safe_load(schema)["slots"]["alias"]
    assert alias["maximum_cardinality"] == 1
    assert "multivalued" not in alias


def test_linkml_rejects_slot_specs_for_undeclared_slots():
    with pytest.raises(ValueError, match="undeclared slot"):
        build_linkml_schema("hello", {"Person": ["name"]}, slot_specs={"unknown": {"enum": ["x"]}})


@pytest.mark.parametrize(
    "spec",
    [
        {"minimum_cardinality": -1},
        {"maximum_cardinality": -1},
        {"minimum_cardinality": 3, "maximum_cardinality": 2},
    ],
)
def test_linkml_rejects_invalid_cardinality(spec):
    with pytest.raises(ValueError, match="cardinality"):
        build_linkml_schema("hello", {"Person": ["aliases"]}, slot_specs={"aliases": spec})
