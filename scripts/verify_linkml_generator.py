"""Verify the optional LinkML generator against the checked-in fixtures."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def verify(schema_path: Path, valid_path: Path, invalid_path: Path) -> dict[str, object]:
    """Generate JSON Schema and prove the valid/invalid fixture split."""
    executable = shutil.which("gen-json-schema")
    if executable is None:
        raise RuntimeError("gen-json-schema is not installed; install requirements/optional.lock first")
    try:
        import yaml
        from jsonschema import Draft202012Validator
    except ImportError as exc:  # pragma: no cover - optional environment only
        raise RuntimeError("PyYAML and jsonschema are required for the optional LinkML check") from exc
    with tempfile.TemporaryDirectory(prefix="ontokit-linkml-") as temporary:
        generated = Path(temporary) / "schema.json"
        command = [executable, "--top-class", "Person", "--closed", str(schema_path)]
        with generated.open("w", encoding="utf-8") as handle:
            subprocess.run(command, check=True, stdout=handle, stderr=subprocess.PIPE, text=True)
        schema = json.loads(generated.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        valid_errors = list(validator.iter_errors(yaml.safe_load(valid_path.read_text(encoding="utf-8"))))
        invalid_errors = list(validator.iter_errors(yaml.safe_load(invalid_path.read_text(encoding="utf-8"))))
    if valid_errors or not invalid_errors:
        raise AssertionError(f"LinkML fixture split failed: valid_errors={len(valid_errors)}, invalid_errors={len(invalid_errors)}")
    return {
        "generator": executable,
        "schema": str(schema_path),
        "valid": True,
        "invalid_rejected": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schema", type=Path, default=Path("docs/reference/linkml-fixtures/hello.yaml"))
    parser.add_argument("--valid", type=Path, default=Path("docs/reference/linkml-fixtures/valid.yaml"))
    parser.add_argument("--invalid", type=Path, default=Path("docs/reference/linkml-fixtures/invalid.yaml"))
    args = parser.parse_args()
    print(json.dumps(verify(args.schema, args.valid, args.invalid), indent=2))


if __name__ == "__main__":
    main()
