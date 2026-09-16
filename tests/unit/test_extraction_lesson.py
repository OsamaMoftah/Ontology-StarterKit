from scripts.run_extraction_lesson import run


def test_extraction_lesson_retains_spans_and_requires_trusted_write():
    result = run("examples/life-science-annotations/extraction-lesson.yaml")
    assert result["candidate_rdf_conforms"] is True
    assert result["validation_errors"] == []
    assert result["review_diff"]["trusted_write_required"] is True
    assert all(candidate["source_id"] == "passage-001" for candidate in result["candidates"])
