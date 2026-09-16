"""Offline RDF, SHACL and named competency-question utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from pyshacl import validate
from rdflib import Graph

from .packs import Pack, PackError


@dataclass(frozen=True)
class ValidationReport:
    """A compact, serializable validation result."""

    conforms: bool
    messages: tuple[str, ...]


def load_graph(path: str | Path) -> Graph:
    """Parse a Turtle/RDF file into an RDFLib graph."""
    graph = Graph()
    try:
        graph.parse(path)
    except Exception as exc:  # rdflib exposes parser-specific exception types
        raise PackError(f"could not parse RDF data: {path}") from exc
    return graph


def validate_pack(pack: Pack, *, data_path: str | None = None) -> ValidationReport:
    """Validate pack data with SHACL and reject empty datasets."""
    data = load_graph(pack.resolve(data_path or pack.manifest.get("data", "data.ttl")))
    if len(data) == 0:
        return ValidationReport(False, ("data graph is empty; target coverage cannot be established",))
    shapes = load_graph(pack.resolve(str(pack.manifest["shapes"])))
    conforms, report_graph, report_text = validate(data, shacl_graph=shapes)
    messages = tuple(str(report_text).splitlines())
    if not conforms and not messages:
        messages = ("SHACL validation failed",)
    return ValidationReport(bool(conforms), messages)


def run_named_query(pack: Pack, query_id: str, *, data_path: str | None = None, parameters: dict[str, Any] | None = None) -> list[dict[str, str]]:
    """Run a manifest-declared SPARQL query, with no arbitrary query input."""
    queries = pack.manifest.get("queries", {})
    if query_id not in queries:
        raise PackError(f"unknown named query: {query_id}")
    if parameters:
        raise PackError("query parameters are not supported by this offline runner")
    data = load_graph(pack.resolve(data_path or pack.manifest.get("data", "data.ttl")))
    query = pack.resolve(str(queries[query_id])).read_text()
    rows: list[dict[str, str]] = []
    for result in data.query(query):
        row = cast(Any, result).asdict()
        rows.append({str(variable): str(value) for variable, value in row.items()})
    return rows
