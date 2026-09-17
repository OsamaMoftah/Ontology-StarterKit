import pytest

from ontology_starterkit.neo4j_queries import enforce_result_limits, prepare_named_query


def test_named_query_is_parameterized_and_bounded():
    query, params = prepare_named_query("people_managing_teams", {"manages_predicate": "https://example.test/manages", "limit": 10})
    assert "$manages_predicate" in query
    assert "example.test" in params["manages_predicate"]
    with pytest.raises(ValueError):
        prepare_named_query("people_managing_teams", {"manages_predicate": "https://example.test/manages", "limit": 101})


def test_named_query_rejects_unknown_or_mistyped_parameters():
    with pytest.raises(ValueError):
        prepare_named_query("people_managing_teams", {"manages_predicate": "x", "limit": 1})
    with pytest.raises(TypeError):
        prepare_named_query("people_managing_teams", {"manages_predicate": "https://example.test/manages", "limit": "1"})


def test_result_limits_bound_rows_and_bytes():
    with pytest.raises(ValueError, match="rows"):
        enforce_result_limits([{"x": 1}, {"x": 2}], max_rows=1, max_bytes=1000)
    with pytest.raises(ValueError, match="bytes"):
        enforce_result_limits([{"x": "long"}], max_rows=1, max_bytes=2)
