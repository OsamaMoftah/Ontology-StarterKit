from ontology_starterkit.evidence import build_answer


def test_build_answer_includes_only_declared_evidence_ids():
    result = build_answer(
        answer="Maya Chen",
        evidence_ids=["ex:Maya", "ex:Aurora"],
        allowed_evidence_ids={"ex:Maya", "ex:Aurora", "ex:Alpha"},
        data_version="hello-ontology@0.2.0",
    )
    assert result.status == "supported"
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
