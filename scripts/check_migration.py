"""Check a declared ontology migration mapping for old query compatibility."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
import argparse
import json
from pathlib import Path

import yaml


@dataclass(frozen=True)
class Migration:
    old_version: str
    new_version: str
    compatible: tuple[str, ...]
    breaking: tuple[str, ...]
    replacements: dict[str, str]


def validate_migration(migration: Migration, existing_queries: Iterable[str]) -> list[str]:
    errors: list[str] = []
    if migration.old_version == migration.new_version:
        errors.append("migration versions must differ")
    queries = set(existing_queries)
    for query in migration.compatible:
        if query not in queries:
            errors.append(f"compatible query is missing: {query}")
    for old, new in migration.replacements.items():
        if not old or not new:
            errors.append("replacement mappings require old and new identifiers")
    overlap = set(migration.compatible) & set(migration.breaking)
    if overlap:
        errors.append(f"query classified as both compatible and breaking: {sorted(overlap)}")
    return errors


def load_migration(path: str | Path) -> Migration:
    value = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return Migration(
        old_version=str(value["old_version"]),
        new_version=str(value["new_version"]),
        compatible=tuple(value.get("compatible", ())),
        breaking=tuple(value.get("breaking", ())),
        replacements={str(key): str(item) for key, item in value.get("replacements", {}).items()},
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mapping", type=Path)
    parser.add_argument("--query", action="append", default=[])
    args = parser.parse_args()
    errors = validate_migration(load_migration(args.mapping), args.query)
    print(json.dumps({"valid": not errors, "errors": errors}, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
