"""Seed a local Neo4j instance with a pack's RDF triples.

This is intentionally a small development helper. It refuses non-local hosts,
uses MERGE for idempotence, and never drops existing data.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from urllib.parse import urlparse

from ontology_starterkit.packs import load_pack
from ontology_starterkit.validation import load_graph


def _local_uri(uri: str) -> bool:
    host = urlparse(uri).hostname
    return host in {"localhost", "127.0.0.1", "::1"}


def seed(pack_path: str | Path, *, uri: str | None = None, database: str = "neo4j") -> int:
    """Insert RDF triples as generic Resource/Triple nodes and return a count."""
    uri = uri or os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
    if not _local_uri(uri):
        raise ValueError("seed helper only permits a local Neo4j URI")
    try:
        from neo4j import GraphDatabase
    except ImportError as exc:  # pragma: no cover - requires optional service extra
        raise RuntimeError("install ontology-starterkit[graphrag] to seed Neo4j") from exc

    pack = load_pack(pack_path)
    graph = load_graph(pack.resolve(str(pack.manifest.get("data", "data.ttl"))))
    username = os.getenv("NEO4J_USERNAME", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "starterkit-local-only")
    driver = GraphDatabase.driver(uri, auth=(username, password), connection_timeout=5)
    count = 0
    try:
        with driver.session(database=database) as session:
            for subject, predicate, object_ in graph:
                session.run(
                    """
                    MERGE (s:Resource {iri: $subject})
                    MERGE (o:Resource {iri: $object})
                    MERGE (s)-[:TRIPLE {predicate: $predicate}]->(o)
                    """,
                    subject=str(subject), predicate=str(predicate), object=str(object_),
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

