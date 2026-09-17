from pathlib import Path

from scripts.check_migration import load_migration, validate_migration


ROOT = Path(__file__).resolve().parents[2]


def test_declared_migration_has_safe_and_breaking_paths():
    migration = load_migration(ROOT / "docs/migrations/0.2-to-0.3.yaml")
    assert validate_migration(migration, {"manager", "owner", "evidence"}) == []
    assert migration.old_version == "0.2.0"
    assert migration.new_version == "0.3.0"
