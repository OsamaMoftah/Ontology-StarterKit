import pytest
import shutil
import subprocess
import sys
from pathlib import Path
import yaml
from jsonschema.exceptions import ValidationError

from ontology_starterkit.linkml import build_linkml_schema
from scripts.verify_linkml_generator import _require_error

ROOT = Path(__file__).resolve().parents[2]


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


def test_linkml_renders_zero_maximum_as_an_empty_collection():
    schema = build_linkml_schema(
        "hello", {"Person": ["alias"]},
        slot_specs={"alias": {"maximum_cardinality": 0}},
    )
    alias = yaml.safe_load(schema)["slots"]["alias"]
    assert alias["maximum_cardinality"] == 0
    assert alias["multivalued"] is True


def test_linkml_generator_verifies_cardinality_and_enum_failures_separately():
    if shutil.which("gen-json-schema") is None:
        pytest.skip("gen-json-schema is not installed")
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/verify_linkml_generator.py"),
            "--schema", str(ROOT / "docs/reference/linkml-fixtures/hello.yaml"),
            "--valid", str(ROOT / "docs/reference/linkml-fixtures/valid.yaml"),
            "--invalid-cardinality", str(ROOT / "docs/reference/linkml-fixtures/invalid.yaml"),
            "--invalid-enum", str(ROOT / "docs/reference/linkml-fixtures/invalid-enum.yaml"),
            "--zero-max-schema", str(ROOT / "docs/reference/linkml-fixtures/zero-max.yaml"),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_linkml_generator_verifier_rejects_unexpected_validation_errors():
    expected = ValidationError("too many aliases", validator="maxItems", path=["aliases"])
    unexpected = ValidationError("unknown status", validator="enum", path=["status"])
    with pytest.raises(AssertionError, match="exactly"):
        _require_error(
            [expected, unexpected],
            validator="maxItems",
            path=["aliases"],
            fixture=ROOT / "invalid.yaml",
        )


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
