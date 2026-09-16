"""Small bounded runtime for the allowlisted Neo4j query templates."""

from __future__ import annotations

import time
from typing import Any

from .neo4j_queries import enforce_result_limits, prepare_named_query


def run_named_query(session: Any, name: str, parameters: dict[str, Any], *, timeout_seconds: float = 5.0, max_bytes: int = 64_000) -> list[dict[str, Any]]:
    """Run one named query with a database timeout and bounded result serialization."""
    query, checked = prepare_named_query(name, parameters)
    started = time.monotonic()
    result = session.run(query, **checked, timeout=timeout_seconds)
    rows = [record.data() for record in result]
    if time.monotonic() - started > timeout_seconds:
        raise TimeoutError("Neo4j query exceeded client deadline")
    return enforce_result_limits(rows, max_rows=checked.get("limit", 100), max_bytes=max_bytes)
