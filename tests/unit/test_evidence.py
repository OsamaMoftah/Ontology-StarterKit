from rdflib import Graph, URIRef
from ontology_starterkit.evidence import build_answer, build_verified_answer


def test_build_answer_includes_only_declared_evidence_ids():
    result = build_answer(
        answer="Maya Chen",
        evidence_ids=["ex:Maya", "ex:Aurora"],
        allowed_evidence_ids={"ex:Maya", "ex:Aurora", "ex:Alpha"},
        data_version="hello-ontology@0.2.0",
    )
    assert result.status == "unverified"
    assert result.evidence_ids == ("ex:Maya", "ex:Aurora")
    assert result.data_version == "hello-ontology@0.2.0"


def test_build_answer_abstains_when_evidence_is_missing():
    result = build_answer(
        answer="Maya Chen",
        evidence_ids=[],
        allowed_evidence_ids={"ex:Maya"},
        data_version="demo@1",
    )
    assert result.status == "insufficient-evidence"
    assert result.answer == "Insufficient evidence in this dataset."


def test_build_answer_rejects_unknown_citation():
    try:
        build_answer("answer", ["ex:Unknown"], {"ex:Known"}, "demo@1")
    except ValueError as exc:
        assert "evidence" in str(exc).lower()
    else:
        raise AssertionError("unknown evidence should be rejected")


def test_build_answer_requires_supporting_assertion_paths_when_provided():
    result = build_answer(
        "Maya Chen", ["ex:Maya"], {"ex:Maya"}, "demo@1", evidence_paths={"ex:Maya": ("ex:Maya", "ex:name")}
    )
    assert result.status == "unverified"
    assert result.support_paths == (("ex:Maya", "ex:name"),)
    abstained = build_answer("Maya Chen", ["ex:Maya"], {"ex:Maya"}, "demo@1", evidence_paths={})
    assert abstained.status == "insufficient-evidence"


def test_verified_answer_requires_actual_graph_paths():
    graph = Graph()
    triple = (URIRef("urn:maya"), URIRef("urn:name"), URIRef("urn:maya-name"))
    graph.add(triple)
    result = build_verified_answer("Maya", ["claim-1"], graph, {"claim-1": (triple,)}, "demo@1", source_records={"claim-1": "crm-7"}, source_spans={"claim-1": "p1:4-8"})
    assert result.status == "supported"
    assert result.graph_path_valid is True
    assert result.source_records == (("claim-1", "crm-7"),)
    assert result.source_support == "reviewed"
    missing = build_verified_answer("Maya", ["claim-1"], graph, {"claim-1": ()}, "demo@1")
    assert missing.status == "insufficient-evidence"
