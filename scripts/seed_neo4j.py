"""Seed a local Neo4j instance with a pack's RDF triples.

This is intentionally a small development helper. It refuses non-local hosts,
uses MERGE for idempotence, and never drops existing data.
"""

from __future__ import annotations

import argparse
import os
from hashlib import sha256
from pathlib import Path
from urllib.parse import urlparse

from rdflib import BNode, Graph, Literal, URIRef
from rdflib.compare import to_canonical_graph

from ontology_starterkit.packs import load_pack
from ontology_starterkit.validation import load_graph


def _local_uri(uri: str) -> bool:
    host = urlparse(uri).hostname
    return host in {"localhost", "127.0.0.1", "::1"}


def scoped_graph(graph: Graph, scope: str) -> Graph:
    """Canonicalize blank nodes for repeat imports, with a pack-specific scope."""
    result = Graph()
    prefix = sha256(scope.encode()).hexdigest()
    for subject, predicate, object_ in to_canonical_graph(graph):
        if isinstance(subject, BNode):
            subject = BNode(f"{prefix}-{subject}")
        if isinstance(object_, BNode):
            object_ = BNode(f"{prefix}-{object_}")
        result.add((subject, predicate, object_))
    return result


def term_payload(term: object) -> dict[str, str]:
    """Preserve RDFLib term kinds and literal metadata in a node payload."""
    if isinstance(term, Literal):
        return {
            "kind": "literal",
            "key": f"literal:{term.n3()}",
            "value": str(term),
            "datatype": str(term.datatype or ""),
            "language": str(term.language or ""),
        }
    if isinstance(term, BNode):
        return {"kind": "blank-node", "key": f"bnode:{term}"}
    if isinstance(term, URIRef):
        return {"kind": "resource", "key": str(term), "iri": str(term)}
    return {"kind": "resource", "key": str(term), "iri": str(term)}


def seed(pack_path: str | Path, *, uri: str | None = None, database: str = "neo4j") -> int:
    """Insert RDF triples while preserving resource, blank-node and literal terms."""
    uri = uri or os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
    if not _local_uri(uri):
        raise ValueError("seed helper only permits a local Neo4j URI")
    try:
        from neo4j import GraphDatabase
    except ImportError as exc:  # pragma: no cover - requires optional service extra
        raise RuntimeError("install ontology-starterkit[graphrag] to seed Neo4j") from exc

    pack = load_pack(pack_path)
    graph = load_graph(pack.resolve(str(pack.manifest.get("data", "data.ttl"))))
    graph = scoped_graph(graph, pack.pack_id)
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "starterkit-local-only")
    driver = GraphDatabase.driver(uri, auth=(username, password), connection_timeout=5)
    count = 0
    try:
        with driver.session(database=database) as session:
            for subject, predicate, object_ in graph:
                subject_payload = term_payload(subject)
                object_payload = term_payload(object_)
                session.run(
                    """
                    MERGE (s:RDFTerm {key: $subject_key})
                    SET s.kind = $subject_kind, s.iri = $subject_iri
                    MERGE (o:RDFTerm {key: $object_key})
                    SET o.kind = $object_kind, o.iri = $object_iri,
                        o.value = $object_value, o.datatype = $object_datatype,
                        o.language = $object_language
                    MERGE (s)-[:TRIPLE {predicate: $predicate}]->(o)
                    """,
                    subject_key=subject_payload["key"], subject_kind=subject_payload["kind"], subject_iri=subject_payload.get("iri"),
                    object_key=object_payload["key"], object_kind=object_payload["kind"], object_iri=object_payload.get("iri"),
                    object_value=object_payload.get("value"), object_datatype=object_payload.get("datatype"), object_language=object_payload.get("language"),
                    predicate=str(predicate),
                ).consume()
                count += 1
    finally:
        driver.close()
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pack", type=Path, help="pack directory to seed")
    parser.add_argument("--uri", default=None, help="local Neo4j URI (default: NEO4J_URI or localhost)")
    parser.add_argument("--database", default="neo4j")
    args = parser.parse_args()
    print(f"Seeded {seed(args.pack, uri=args.uri, database=args.database)} triples")


if __name__ == "__main__":
    main()
