import json
from pathlib import Path

from rdflib import Graph, URIRef
from ontology_starterkit.evidence import assess_answer, build_answer, build_verified_answer, verify_source_spans


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
    assert result.source_support == "unverified"
    assert result.source_span_valid is False
    missing = build_verified_answer("Maya", ["claim-1"], graph, {"claim-1": ()}, "demo@1")
    assert missing.status == "insufficient-evidence"


def test_build_verified_answer_never_infers_review_from_fabricated_source_metadata():
    graph = Graph()
    triple = (URIRef("urn:claim"), URIRef("urn:supports"), URIRef("urn:evidence"))
    graph.add(triple)

    result = build_verified_answer(
        "the claim",
        ["claim-1"],
        graph,
        {"claim-1": (triple,)},
        "demo@1",
        source_records={"claim-1": "fabricated-record"},
        source_spans={"claim-1": "missing-document@0:999999"},
    )

    assert result.status == "supported"
    assert result.graph_path_valid is True
    assert result.source_support == "unverified"
    assert result.source_span_valid is False


def test_assess_answer_separates_path_validity_from_source_support():
    graph = Graph()
    triple = (URIRef("urn:claim"), URIRef("urn:supports"), URIRef("urn:evidence"))
    graph.add(triple)
    result = assess_answer(
        "the claim",
        ["claim-1"],
        {"claim-1"},
        graph,
        {"claim-1": (triple,)},
        "demo@1",
        source_states={"claim-1": "unknown"},
    )
    assert result.graph_path_valid is True
    assert result.source_support == "unknown"
    assert result.status == "unsupported"
    assert result.answer_correctness == "unverified"


def test_assess_answer_reports_conflicting_and_stale_evidence():
    graph = Graph()
    triple = (URIRef("urn:claim"), URIRef("urn:supports"), URIRef("urn:evidence"))
    graph.add(triple)
    paths = {"claim-1": (triple,)}
    conflicting = assess_answer("claim", ["claim-1"], {"claim-1"}, graph, paths, "demo@1", source_states={"claim-1": "conflicting"})
    stale = assess_answer("claim", ["claim-1"], {"claim-1"}, graph, paths, "demo@1", source_states={"claim-1": "stale"})
    assert conflicting.status == "conflicting"
    assert conflicting.source_support == "conflicting"
    assert stale.status == "stale"
    assert stale.source_support == "stale"


def test_assess_answer_rejects_valid_citation_with_invalid_graph_path():
    graph = Graph()
    result = assess_answer(
        "claim",
        ["claim-1"],
        {"claim-1"},
        graph,
        {"claim-1": ((URIRef("urn:missing"), URIRef("urn:p"), URIRef("urn:o")),)},
        "demo@1",
        source_states={"claim-1": "supported"},
    )
    assert result.status == "insufficient-evidence"
    assert result.graph_path_valid is False
    assert result.source_support == "unverified"


def test_assess_answer_can_record_answer_correctness_separately():
    graph = Graph()
    triple = (URIRef("urn:claim"), URIRef("urn:supports"), URIRef("urn:evidence"))
    graph.add(triple)
    result = assess_answer(
        "wrong answer",
        ["claim-1"],
        {"claim-1"},
        graph,
        {"claim-1": (triple,)},
        "demo@1",
        source_states={"claim-1": "supported"},
        answer_correct=False,
    )
    assert result.status == "unsupported"
    assert result.source_support == "reviewed"
    assert result.answer_correctness == "incorrect"


def test_reviewed_evidence_evaluation_fixture_covers_each_outcome():
    path = Path(__file__).resolve().parents[2] / "examples/consulting-evidence-room/expected/evidence-assessment.json"
    cases = json.loads(path.read_text(encoding="utf-8"))
    assert {item["outcome"] for item in cases} == {"supported", "unsupported", "conflicting", "stale", "insufficient-evidence"}


def test_source_span_offsets_are_checked_against_the_source_document():
    documents = {"packet-v2": "Asset A has a reviewed target hypothesis."}
    assert verify_source_spans({"claim-1": "packet-v2@0:8"}, documents) == ("claim-1",)
    assert verify_source_spans({"claim-1": "packet-v2@0:999"}, documents) == ()
    graph = Graph()
    triple = (URIRef("urn:claim"), URIRef("urn:supports"), URIRef("urn:evidence"))
    graph.add(triple)
    invalid = assess_answer(
        "claim", ["claim-1"], {"claim-1"}, graph, {"claim-1": (triple,)}, "demo@1",
        source_states={"claim-1": "supported"}, source_spans={"claim-1": "packet-v2@0:999"}, source_documents=documents,
    )
    assert invalid.status == "insufficient-evidence"
    assert invalid.source_span_valid is False
