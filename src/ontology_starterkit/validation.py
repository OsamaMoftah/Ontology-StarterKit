"""Offline RDF, SHACL and named competency-question utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast
from pyparsing import ParseResults

from pyshacl import validate
from rdflib import Graph, RDF
from rdflib.namespace import SH
from rdflib.plugins.sparql.parser import parseQuery
from rdflib.plugins.sparql.parserutils import CompValue

from .packs import Pack, PackError


def validate_named_query(query: str) -> None:
    """Accept one local SELECT; reject dataset loading and federated queries."""
    try:
        parsed = parseQuery(query)
    except Exception as exc:
        raise PackError("named query must be one valid local read SELECT operation") from exc
    if parsed[1].name != "SelectQuery":
        raise PackError("named query must be a local read SELECT operation")

    def inspect(value: Any) -> None:
        if isinstance(value, CompValue):
            if value.name in {"ServiceGraphPattern", "DatasetClause"}:
                raise PackError("named queries may only contain one local read operation; SERVICE and FROM are forbidden")
            for item in value.values():
                inspect(item)
        elif isinstance(value, (list, tuple, ParseResults)):
            for item in value:
                inspect(item)

    inspect(parsed)


@dataclass(frozen=True)
class ValidationReport:
    """A compact, serializable validation result."""

    conforms: bool
    messages: tuple[str, ...]


def load_graph(path: str | Path) -> Graph:
    """Parse a Turtle/RDF file into an RDFLib graph."""
    graph = Graph()
    try:
        graph.parse(path, format="turtle")
    except Exception as exc:  # rdflib exposes parser-specific exception types
        raise PackError(f"could not parse RDF data: {path}") from exc
    return graph


def validate_pack(pack: Pack, *, data_path: str | None = None) -> ValidationReport:
    """Validate pack data with SHACL and reject empty datasets."""
    data = load_graph(pack.resolve(data_path or pack.manifest.get("data", "data.ttl")))
    if len(data) == 0:
        return ValidationReport(False, ("data graph is empty; target coverage cannot be established",))
    shapes = load_graph(pack.resolve(str(pack.manifest["shapes"])))
    uncovered: list[str] = []
    for shape in shapes.subjects(RDF.type, SH.NodeShape):
        target_classes = list(shapes.objects(shape, SH.targetClass))
        target_predicates = list(shapes.objects(shape, SH.targetSubjectsOf))
        if target_classes and not any((None, RDF.type, target) in data for target in target_classes):
            uncovered.append(f"{shape} targetClass has no matching data")
        if target_predicates and not any((None, predicate, None) in data for predicate in target_predicates):
            uncovered.append(f"{shape} targetSubjectsOf has no matching data")
    if uncovered:
        return ValidationReport(False, ("data graph has no instances for declared SHACL targets", *uncovered))
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
    validate_named_query(query)
    rows: list[dict[str, str]] = []
    for result in data.query(query):
        row = cast(Any, result).asdict()
        rows.append({str(variable): str(value) for variable, value in row.items()})
    return rows
