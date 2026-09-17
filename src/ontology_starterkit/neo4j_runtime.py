"""Small bounded runtime for the allowlisted Neo4j query templates."""

from __future__ import annotations

import time
from typing import Any

from .neo4j_queries import enforce_result_limits, prepare_named_query


def run_named_query(session: Any, name: str, parameters: dict[str, Any], *, timeout_seconds: float = 5.0, max_bytes: int = 64_000) -> list[dict[str, Any]]:
    """Run one named query with a server transaction timeout and bounded output.

    Neo4j's Python driver does not apply a ``timeout`` keyword passed to
    ``Session.run`` as a server transaction timeout; it becomes a Cypher
    parameter. The explicit transaction below is therefore required for the
    database to terminate an over-budget query.
    """
    query, checked = prepare_named_query(name, parameters)
    started = time.monotonic()
    transaction = session.begin_transaction(timeout=timeout_seconds)
    try:
        result = transaction.run(query, checked)
        rows = [record.data() for record in result]
        transaction.commit()
    except Exception:
        try:
            transaction.rollback()
        finally:
            transaction.close()
        raise
    transaction.close()
    if time.monotonic() - started > timeout_seconds:
        raise TimeoutError("Neo4j query exceeded client deadline")
    return enforce_result_limits(rows, max_rows=checked.get("limit", 100), max_bytes=max_bytes)
