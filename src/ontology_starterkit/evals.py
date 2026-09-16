"""Small, deterministic evaluation helpers for ontology packs."""

from __future__ import annotations

import json
from collections import Counter
from typing import Any

from .packs import Pack, PackError
from .validation import run_named_query


def load_expected(pack: Pack, query_id: str) -> list[dict[str, str]]:
    """Load expected rows declared by a pack, if present."""
    expected = pack.manifest.get("expected", {})
    path = expected.get(query_id)
    if not path:
        raise PackError(f"no expected output declared for query: {query_id}")
    try:
        value: Any = json.loads(pack.resolve(str(path)).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise PackError(f"could not read expected output for query: {query_id}") from exc
    if isinstance(value, dict) and isinstance(value.get("bindings"), list):
        value = value["bindings"]
    if not isinstance(value, list) or not all(isinstance(row, dict) for row in value):
        raise PackError(f"expected output must be a list of objects or a bindings fixture: {query_id}")
    return [{str(key): str(item) for key, item in row.items()} for row in value]


def evaluate_query(pack: Pack, query_id: str) -> dict[str, object]:
    """Compare a named query with its fixture and return a JSON-safe report."""
    actual = run_named_query(pack, query_id)
    expected = load_expected(pack, query_id)
    actual_set = Counter(tuple(sorted(row.items())) for row in actual)
    expected_set = Counter(tuple(sorted(row.items())) for row in expected)
    missing = [dict(row) for row in sorted((expected_set - actual_set).elements())]
    unexpected = [dict(row) for row in sorted((actual_set - expected_set).elements())]
    return {
        "pack": pack.pack_id,
        "query": query_id,
        "passed": not missing and not unexpected,
        "actual_count": len(actual),
        "expected_count": len(expected),
        "missing": missing,
        "unexpected": unexpected,
    }
