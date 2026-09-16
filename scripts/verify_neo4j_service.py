"""Verify the local Neo4j read-only and cancellation contract.

This script is intentionally opt-in: it changes only the local Compose
database named by the supplied credentials and removes its probe data/user.
"""

from __future__ import annotations

import argparse
import os

from ontology_starterkit.neo4j_runtime import run_named_query


def verify(uri: str, admin_user: str, admin_password: str, *, database: str = "neo4j") -> dict[str, bool]:
    try:
        from neo4j import GraphDatabase
        from neo4j.exceptions import Neo4jError
    except ImportError as exc:  # pragma: no cover - optional environment
        raise RuntimeError("install the graphrag extra to run the Neo4j service check") from exc

    reader = "starterkit_reader"
    reader_password = os.getenv("ONTOLOGY_READER_PASSWORD", "starterkit-reader-local")
    admin_driver = GraphDatabase.driver(uri, auth=(admin_user, admin_password), connection_timeout=5)
    read_denied = False
    cancelled = False
    try:
        with admin_driver.session(database=database) as session:
            try:
                session.run("CREATE USER starterkit_reader SET PASSWORD $password CHANGE NOT REQUIRED", password=reader_password).consume()
                session.run("GRANT ROLE reader TO starterkit_reader").consume()
            except Neo4jError as exc:
                if "Unsupported administration command" in str(exc):
                    raise RuntimeError("the configured Neo4j edition does not expose database role grants; use a licensed Enterprise service to prove database-enforced read-only access") from exc
                raise
            session.run(
                "MERGE (s:RDFTerm {key: $s}) MERGE (o:RDFTerm {key: $o}) MERGE (s)-[:TRIPLE {predicate: $p, scope: 'verify'}]->(o)",
                s="https://ontology-starterkit.dev/verify/Maya", o="https://ontology-starterkit.dev/verify/Aurora",
                p="https://ontology-starterkit.dev/business/manages",
            ).consume()

        reader_driver = GraphDatabase.driver(uri, auth=(reader, reader_password), connection_timeout=5)
        try:
            with reader_driver.session(database=database) as session:
                rows = run_named_query(session, "people_managing_teams", {
                    "manages_predicate": "https://ontology-starterkit.dev/business/manages", "limit": 10,
                }, timeout_seconds=5)
                if not rows:
                    raise RuntimeError("named read query returned no seeded rows")
                try:
                    session.run("CREATE (:StarterKitWriteProbe)").consume()
                except Neo4jError:
                    read_denied = True
                else:
                    raise RuntimeError("reader account was able to write")
                try:
                    session.run("UNWIND range(1, 10000000) AS n RETURN count(n)", timeout=0.001).consume()
                except Neo4jError:
                    cancelled = True
        finally:
            reader_driver.close()
    finally:
        with admin_driver.session(database=database) as session:
            session.run("MATCH (s:RDFTerm)-[r:TRIPLE {scope: 'verify'}]->() DELETE r").consume()
            session.run("DROP USER starterkit_reader").consume()
        admin_driver.close()
    return {"named_query": True, "write_denied": read_denied, "server_cancelled": cancelled}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--uri", default=os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687"))
    parser.add_argument("--user", default=os.getenv("NEO4J_USERNAME", "neo4j"))
    parser.add_argument("--password", default=os.getenv("NEO4J_PASSWORD", "starterkit-local-only"))
    parser.add_argument("--database", default="neo4j")
    args = parser.parse_args()
    print(verify(args.uri, args.user, args.password, database=args.database))


if __name__ == "__main__":
    main()
