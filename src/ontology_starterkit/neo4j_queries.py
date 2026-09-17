"""Allowlisted, parameterized Cypher templates for the supported Neo4j path."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Mapping


@dataclass(frozen=True)
class QuerySpec:
    name: str
    cypher: str
    parameters: Mapping[str, type]
    max_rows: int = 100


QUERY_SPECS = {
    "people_managing_teams": QuerySpec(
        "people_managing_teams",
        "MATCH (person:RDFTerm)-[:TRIPLE {predicate: $manages_predicate}]->(team:RDFTerm) RETURN person.key AS person, team.key AS team LIMIT $limit",
        {"manages_predicate": str, "limit": int},
    ),
    "claims_with_evidence": QuerySpec(
        "claims_with_evidence",
        "MATCH (claim:RDFTerm)-[:TRIPLE {predicate: $supports_predicate}]->(evidence:RDFTerm) RETURN claim.key AS claim, evidence.key AS evidence LIMIT $limit",
        {"supports_predicate": str, "limit": int},
    ),
}


def prepare_named_query(name: str, parameters: Mapping[str, Any]) -> tuple[str, dict[str, Any]]:
    """Validate an allowlisted template and return Cypher plus safe parameters."""
    if name not in QUERY_SPECS:
        raise ValueError(f"unknown named Neo4j query: {name}")
    spec = QUERY_SPECS[name]
    missing = set(spec.parameters) - set(parameters)
    extra = set(parameters) - set(spec.parameters)
    if missing or extra:
        raise ValueError(f"invalid parameters; missing={sorted(missing)}, extra={sorted(extra)}")
    checked: dict[str, Any] = {}
    for key, expected in spec.parameters.items():
        value = parameters[key]
        if expected is int:
            if type(value) is not int:
                raise TypeError(f"parameter {key} must be int")
            if key == "limit" and not 1 <= value <= spec.max_rows:
                raise ValueError(f"parameter limit must be between 1 and {spec.max_rows}")
        elif expected is str:
            if type(value) is not str:
                raise TypeError(f"parameter {key} must be str")
            if key.endswith("predicate") and not re.fullmatch(r"https?://[^\s<>]+", value):
                raise ValueError(f"parameter {key} must be an absolute predicate IRI")
        else:
            raise TypeError(f"unsupported parameter type for {key}")
        checked[key] = value
    return spec.cypher, checked


def enforce_result_limits(rows: list[Mapping[str, Any]], *, max_rows: int, max_bytes: int) -> list[dict[str, Any]]:
    """Bound row count and serialized response size before returning results."""
    if len(rows) > max_rows:
        raise ValueError(f"query returned more than {max_rows} rows")
    result = [dict(row) for row in rows]
    size = sum(len(repr(row).encode("utf-8")) for row in result)
    if size > max_bytes:
        raise ValueError(f"query response exceeds {max_bytes} bytes")
    return result
