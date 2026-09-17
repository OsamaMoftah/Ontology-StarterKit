import pytest

from ontology_starterkit.neo4j_runtime import run_named_query


class Record:
    def __init__(self, data): self._data = data
    def data(self): return self._data


class Session:
    def __init__(self):
        self.kwargs = None
        self.tx = Transaction(self)
        self.rows = [{"person": "a", "team": "b"}]
    def begin_transaction(self, **kwargs):
        self.kwargs = kwargs
        return self.tx


class Transaction:
    def __init__(self, session):
        self.session = session
        self.committed = False
    def run(self, query, parameters):
        self.parameters = parameters
        return [Record(row) for row in self.session.rows]
    def commit(self): self.committed = True
    def rollback(self): pass
    def close(self): pass


def test_runtime_passes_database_timeout_and_returns_bounded_rows():
    session = Session()
    rows = run_named_query(session, "people_managing_teams", {"manages_predicate": "https://example.test/manages", "limit": 5})
    assert rows == [{"person": "a", "team": "b"}]
    assert session.kwargs["timeout"] == 5.0
    assert session.tx.committed is True


def test_runtime_rejects_oversized_serialized_results():
    class Large(Session):
        def __init__(self):
            super().__init__()
            self.rows = [{"x": "x" * 100}]
    with pytest.raises(ValueError, match="bytes"):
        run_named_query(Large(), "people_managing_teams", {"manages_predicate": "https://example.test/manages", "limit": 5}, max_bytes=10)
