"""Run the business pack's reviewable identity-mapping exercise."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from ontology_starterkit.entity_resolution import apply_decisions, approve_decision, review_alias_candidates, rollback_decisions


def run(path: str | Path) -> dict[str, object]:
    fixture = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    decisions = review_alias_candidates(
        fixture["records"], fixture["aliases"], field=fixture["field"], mapping_version=fixture["mapping_version"]
    )
    approved = [approve_decision(decision, fixture["reviewer"], approved_on=fixture["approved_on"]) for decision in decisions if decision.status == "queued"]
    applied = apply_decisions(fixture["records"], approved)
    repeated = apply_decisions(applied, approved)
    return {
        "mapping_version": fixture["mapping_version"],
        "queue": [decision.as_dict() for decision in decisions],
        "approved": [decision.as_dict() for decision in approved],
        "applied": applied,
        "idempotent": repeated == applied,
        "rollback": rollback_decisions(applied, approved),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    print(json.dumps(run(args.fixture), indent=2))


if __name__ == "__main__":
    main()
