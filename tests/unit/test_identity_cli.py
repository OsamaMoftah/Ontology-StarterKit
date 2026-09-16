from pathlib import Path

from scripts.reconcile_business_ids import run


ROOT = Path(__file__).resolve().parents[2]


def test_identity_fixture_is_reviewable_idempotent_and_reversible():
    result = run(ROOT / "examples/business-projects/identity-reconciliation.yaml")
    assert result["idempotent"] is True
    assert [item["status"] for item in result["queue"]] == ["queued", "ambiguous", "unmatched"]
    assert result["applied"][0]["team"].endswith("TeamAurora")
    assert result["applied"][1]["team"] == "Aurora"
    assert result["rollback"] == [
        {"id": "crm-001", "team": "Aurora Team"},
        {"id": "hr-002", "team": "Aurora"},
        {"id": "legacy-003", "team": "Unknown Team"},
    ]
