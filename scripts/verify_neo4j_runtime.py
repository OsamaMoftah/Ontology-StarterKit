"""Verify live Neo4j query parity, term fidelity, and server cancellation."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

from rdflib import BNode, Literal

from ontology_starterkit.neo4j_runtime import run_named_query
from ontology_starterkit.packs import load_pack
from ontology_starterkit.validation import load_graph
try:
    from scripts.seed_neo4j import scoped_graph, seed, term_payload
except ModuleNotFoundError:  # pragma: no cover - direct script execution
    from seed_neo4j import scoped_graph, seed, term_payload


def verify(uri: str, username: str, password: str, *, database: str = "neo4j") -> dict[str, Any]:
    """Seed two fixtures and prove the live runtime contract."""
    try:
        from neo4j import GraphDatabase
        from neo4j.exceptions import Neo4jError
    except ImportError as exc:  # pragma: no cover - optional environment
        raise RuntimeError("install the graphrag extra to run the Neo4j runtime check") from exc

    root = Path(__file__).resolve().parents[1]
    business = load_pack(root / "examples/business-projects")
    hello = load_pack(root / "examples/hello-ontology")
    os.environ.update({"NEO4J_URI": uri, "NEO4J_USERNAME": username, "NEO4J_PASSWORD": password})
    seed(business.root, uri=uri, database=database)
    seed(hello.root, uri=uri, database=database)
    business_graph = load_graph(business.resolve(str(business.manifest["data"])))
    expected_pairs = {
        (str(subject), str(object_))
        for subject, predicate, object_ in business_graph
        if str(predicate) == "https://ontology-starterkit.dev/business/manages"
    }

    driver = GraphDatabase.driver(uri, auth=(username, password), connection_timeout=5)
    try:
        with driver.session(database=database) as session:
            rows = run_named_query(
                session,
                "people_managing_teams",
                {"manages_predicate": "https://ontology-starterkit.dev/business/manages", "limit": 10},
            )
            actual_pairs = {(row["person"], row["team"]) for row in rows}
            parity = actual_pairs == expected_pairs

            hello_graph = load_graph(hello.resolve(str(hello.manifest["data"])))
            seeded_hello_graph = scoped_graph(hello_graph, hello.pack_id)
            literals = [term for _, _, term in seeded_hello_graph if isinstance(term, Literal) and term.language]
            blank_nodes = [term for triple in seeded_hello_graph for term in triple if isinstance(term, BNode)]
            literal_fidelity = all(
                session.run(
                    "MATCH (n:RDFTerm {key: $key}) RETURN n.kind AS kind, n.value AS value, n.datatype AS datatype, n.language AS language",
                    key=term_payload(term)["key"],
                ).single().data()["language"] == term.language
                for term in literals
            )
            blank_node_fidelity = all(
                session.run(
                    "MATCH (n:RDFTerm {key: $key}) RETURN n.kind AS kind",
                    key=term_payload(term)["key"],
                ).single().data()["kind"] == "blank-node"
                for term in blank_nodes
            )

            cancelled = False
            transaction = session.begin_transaction(timeout=0.001, metadata={"starterkit_probe": "server-cancel"})
            try:
                transaction.run("UNWIND range(1, 1000000000) AS n RETURN sum(n)", {}).consume()
            except Neo4jError:
                cancelled = True
                try:
                    transaction.rollback()
                except Neo4jError:
                    pass
            finally:
                transaction.close()
            active = session.run(
                "SHOW TRANSACTIONS YIELD metaData, currentQuery "
                "WHERE metaData.starterkit_probe = 'server-cancel' RETURN currentQuery"
            ).data()
            heartbeat = session.run("RETURN 1 AS ok").single()["ok"] == 1
    finally:
        driver.close()
    return {
        "query_parity": parity,
        "expected_rows": len(expected_pairs),
        "actual_rows": len(actual_pairs),
        "literal_language_preserved": literal_fidelity,
        "blank_node_identity_preserved": blank_node_fidelity,
        "repeated_imports_idempotent": seed(business.root, uri=uri, database=database) == len(business_graph),
        "server_cancelled": cancelled and not active,
        "post_cancel_heartbeat": heartbeat,
    }


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
