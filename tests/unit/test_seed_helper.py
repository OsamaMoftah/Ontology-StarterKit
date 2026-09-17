from rdflib import BNode, Literal, URIRef

from scripts.seed_neo4j import _local_uri, graph_delta, term_payload


def test_seed_helper_accepts_only_local_uris():
    assert _local_uri("bolt://localhost:7687") is True
    assert _local_uri("bolt://127.0.0.1:7687") is True
    assert _local_uri("neo4j+s://customer.example") is False


def test_seed_helper_preserves_rdf_term_kinds():
    assert term_payload(URIRef("https://example.test/entity"))["kind"] == "resource"
    literal = term_payload(Literal("42", datatype=URIRef("http://www.w3.org/2001/XMLSchema#integer")))
    assert literal["kind"] == "literal"
    assert literal["value"] == "42"
    assert literal["datatype"].endswith("integer")
    assert term_payload(BNode("b1"))["kind"] == "blank-node"


def test_graph_delta_removes_stale_triples():
    from rdflib import Graph
    previous = Graph().parse(data="<urn:s> <urn:p> <urn:o> .", format="turtle")
    current = Graph().parse(data="<urn:s> <urn:p> <urn:n> .", format="turtle")
    added, removed = graph_delta(previous, current)
    assert len(added) == 1 and len(removed) == 1
