"""Verify the optional LinkML generator against the checked-in fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def _require_error(errors: list[object], *, validator: str, path: list[str], fixture: Path) -> None:
    if not any(getattr(error, "validator", None) == validator and list(getattr(error, "path", ())) == path for error in errors):
        details = [
            (getattr(error, "validator", None), list(getattr(error, "path", ())))
            for error in errors
        ]
        raise AssertionError(
            f"{fixture} did not produce {validator} at {path}; observed {details}"
        )


def _generate_schema(executable: str, schema_path: Path, output_path: Path) -> dict[str, object]:
    command = [executable, "--top-class", "Person", "--closed", str(schema_path)]
    with output_path.open("w", encoding="utf-8") as handle:
        subprocess.run(command, check=True, stdout=handle, stderr=subprocess.PIPE, text=True)
    return json.loads(output_path.read_text(encoding="utf-8"))


def verify(
    schema_path: Path,
    valid_path: Path,
    invalid_cardinality_path: Path,
    invalid_enum_path: Path,
    zero_max_schema_path: Path,
) -> dict[str, object]:
    """Generate JSON Schema and prove each invalid fixture's failure mode."""
    executable = shutil.which("gen-json-schema")
    if executable is None:
        raise RuntimeError("gen-json-schema is not installed; install requirements/optional-py311.lock first")
    try:
        import yaml
        from jsonschema import Draft202012Validator
    except ImportError as exc:  # pragma: no cover - optional environment only
        raise RuntimeError("PyYAML and jsonschema are required for the optional LinkML check") from exc
    with tempfile.TemporaryDirectory(prefix="ontokit-linkml-") as temporary:
        temporary_path = Path(temporary)
        schema = _generate_schema(executable, schema_path, temporary_path / "schema.json")
        validator = Draft202012Validator(schema)
        valid_errors = list(validator.iter_errors(yaml.safe_load(valid_path.read_text(encoding="utf-8"))))
        invalid_cardinality_errors = list(
            validator.iter_errors(yaml.safe_load(invalid_cardinality_path.read_text(encoding="utf-8")))
        )
        invalid_enum_errors = list(
            validator.iter_errors(yaml.safe_load(invalid_enum_path.read_text(encoding="utf-8")))
        )
        zero_validator = Draft202012Validator(
            _generate_schema(executable, zero_max_schema_path, temporary_path / "zero-max-schema.json")
        )
        zero_missing_errors = list(zero_validator.iter_errors({}))
        zero_empty_errors = list(zero_validator.iter_errors({"alias": []}))
        zero_one_errors = list(zero_validator.iter_errors({"alias": ["one"]}))
    if valid_errors:
        raise AssertionError(f"valid LinkML fixture rejected: {len(valid_errors)} errors")
    _require_error(
        invalid_cardinality_errors,
        validator="maxItems",
        path=["aliases"],
        fixture=invalid_cardinality_path,
    )
    _require_error(
        invalid_enum_errors,
        validator="enum",
        path=["status"],
        fixture=invalid_enum_path,
    )
    if any(getattr(error, "validator", None) == "enum" for error in invalid_cardinality_errors):
        raise AssertionError(f"cardinality fixture also failed enum validation: {invalid_cardinality_path}")
    if any(getattr(error, "validator", None) == "maxItems" for error in invalid_enum_errors):
        raise AssertionError(f"enum fixture also failed cardinality validation: {invalid_enum_path}")
    if zero_missing_errors or zero_empty_errors:
        raise AssertionError(
            "zero-maximum schema rejected a missing or empty collection: "
            f"missing={len(zero_missing_errors)}, empty={len(zero_empty_errors)}"
        )
    _require_error(zero_one_errors, validator="maxItems", path=["alias"], fixture=zero_max_schema_path)
    return {
        "generator": executable,
        "schema": str(schema_path),
        "valid": True,
        "cardinality_invalid_rejected": True,
        "enum_invalid_rejected": True,
        "zero_maximum_verified": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, default=Path("docs/reference/linkml-fixtures/hello.yaml"))
    parser.add_argument("--valid", type=Path, default=Path("docs/reference/linkml-fixtures/valid.yaml"))
    parser.add_argument(
        "--invalid-cardinality",
        type=Path,
        default=Path("docs/reference/linkml-fixtures/invalid.yaml"),
    )
    parser.add_argument(
        "--invalid-enum",
        type=Path,
        default=Path("docs/reference/linkml-fixtures/invalid-enum.yaml"),
    )
    parser.add_argument(
        "--zero-max-schema",
        type=Path,
        default=Path("docs/reference/linkml-fixtures/zero-max.yaml"),
    )
    args = parser.parse_args()
    print(
        json.dumps(
            verify(
                args.schema,
                args.valid,
                args.invalid_cardinality,
                args.invalid_enum,
                args.zero_max_schema,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
