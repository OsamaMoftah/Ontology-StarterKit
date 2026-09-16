#!/usr/bin/env python3
"""Verify a Chowlk conversion against a small semantic contract.

The checked-in fixture is intentionally small.  ``--live`` calls the hosted
Chowlk service, while the default mode verifies the expected RDF contract
without requiring network access.  Layout metadata and generated ontology
headers are excluded from the comparison because they are not model semantics.
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

from rdflib import Graph, URIRef


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "docs/reference/chowlk-fixtures/claim-evidence.drawio"
EXPECTED = ROOT / "docs/reference/chowlk-fixtures/expected.ttl"
API_URL = "https://chowlk.linkeddata.es/api"
RDF_TYPE = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
OWL_CLASS = URIRef("http://www.w3.org/2002/07/owl#Class")
RDFS_SUBCLASS = URIRef("http://www.w3.org/2000/01/rdf-schema#subClassOf")


def _model_triples(graph: Graph) -> set[tuple[URIRef, URIRef, URIRef]]:
    """Keep model triples while excluding generated ontology headers."""
    return {
        (subject, predicate, object_)
        for subject, predicate, object_ in graph
        if predicate == RDFS_SUBCLASS or (predicate == RDF_TYPE and object_ == OWL_CLASS)
    }


def _expected_semantics() -> set[tuple[URIRef, URIRef, URIRef]]:
    graph = Graph().parse(EXPECTED, format="turtle")
    return _model_triples(graph)


def _live_turtle(url: str) -> tuple[str, dict]:
    boundary = "----ontology-starterkit-chowlk"
    payload = FIXTURE.read_bytes()
    body = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="data"; filename="claim-evidence.drawio"\r\n'
        "Content-Type: application/xml\r\n\r\n"
    ).encode() + payload + f"\r\n--{boundary}--\r\n".encode()
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        result = json.loads(response.read().decode("utf-8"))
    if result.get("errors"):
        raise SystemExit(f"Chowlk returned diagram errors: {result['errors']}")
    return result["ttl_data"], result


def _semantic_diff(turtle: str) -> dict[str, list[str]]:
    actual = Graph().parse(data=turtle, format="turtle")
    expected = _expected_semantics()
    actual_semantics = _model_triples(actual)
    missing = sorted(" ".join(map(str, triple)) for triple in expected - actual_semantics)
    unexpected = sorted(" ".join(map(str, triple)) for triple in actual_semantics - expected)
    return {"missing": missing, "unexpected": unexpected}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="call the hosted Chowlk API")
    parser.add_argument("--api-url", default=os.environ.get("CHOWLK_API_URL", API_URL))
    args = parser.parse_args()

    if not FIXTURE.exists() or not EXPECTED.exists():
        raise SystemExit("Chowlk fixture files are missing")

    if args.live:
        turtle, response = _live_turtle(args.api_url)
        diff = _semantic_diff(turtle)
        if diff["missing"] or diff["unexpected"]:
            raise SystemExit(json.dumps({"semantic_diff": diff}, indent=2))
        print(json.dumps({"mode": "live", "api": args.api_url, "errors": response.get("errors", {}), "semantic_diff": diff}))
    else:
        diff = _semantic_diff(EXPECTED.read_text())
        if diff["missing"] or diff["unexpected"]:
            raise SystemExit(json.dumps({"semantic_diff": diff}, indent=2))
        print(json.dumps({"mode": "offline-contract", "semantic_diff": diff}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
