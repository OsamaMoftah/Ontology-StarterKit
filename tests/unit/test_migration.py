from scripts.check_migration import Migration, validate_migration


def test_migration_distinguishes_compatible_and_breaking_queries():
    migration = Migration("0.2.0", "0.3.0", ("manager",), ("legacy-owner",), {"OldService": "Service"})
    assert validate_migration(migration, ["manager", "legacy-owner"]) == []


def test_migration_rejects_overlap_and_missing_queries():
    migration = Migration("0.2.0", "0.3.0", ("manager",), ("manager",), {})
    errors = validate_migration(migration, [])
    assert any("missing" in error for error in errors)
    assert any("both" in error for error in errors)
