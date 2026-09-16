import pytest

from ontology_starterkit.neo4j_runtime import run_named_query


class Record:
    def __init__(self, data): self._data = data
    def data(self): return self._data


class Session:
    def __init__(self): self.kwargs = None
    def run(self, query, **kwargs):
        self.kwargs = kwargs
        return [Record({"person": "a", "team": "b"})]


def test_runtime_passes_database_timeout_and_returns_bounded_rows():
    session = Session()
    rows = run_named_query(session, "people_managing_teams", {"manages_predicate": "https://example.test/manages", "limit": 5})
    assert rows == [{"person": "a", "team": "b"}]
    assert session.kwargs["timeout"] == 5.0


def test_runtime_rejects_oversized_serialized_results():
    class Large(Session):
        def run(self, query, **kwargs): return [Record({"x": "x" * 100})]
    with pytest.raises(ValueError, match="bytes"):
        run_named_query(Large(), "people_managing_teams", {"manages_predicate": "https://example.test/manages", "limit": 5}, max_bytes=10)
