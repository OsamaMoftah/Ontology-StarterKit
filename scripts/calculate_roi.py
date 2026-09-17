"""Calculate reproducible ROI scenarios from a JSON fixture."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ontology_starterkit.roi import Scenario, npv, payback_months, roi_percent


def calculate(value: dict[str, object], horizons: list[int], annual_discount_rate: float) -> dict[str, object]:
    labels = [str(item) for item in value.get("benefit_labels", [])]
    benefits = tuple(float(item) for item in value["monthly_benefits"])
    if len(labels) != len(benefits) or len(set(labels)) != len(labels):
        raise ValueError("benefit_labels must be unique and match monthly_benefits")
    scenario = Scenario(
        int(value["build_months"]), float(value["engineering_monthly"]), float(value["sme_monthly"]),
        float(value["infrastructure_monthly"]), float(value["maintenance_monthly"]), benefits,
    )
    return {
        "upfront_cost": scenario.upfront_cost,
        "ongoing_monthly_cost": scenario.ongoing_cost,
        "monthly_value": scenario.monthly_value,
        "net_monthly_benefit": scenario.net_monthly_benefit,
        "payback_months": payback_months(scenario),
        "horizons": {str(months): {"roi_percent": roi_percent(scenario, months), "npv": npv(scenario, months, annual_discount_rate)} for months in horizons},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--rate", type=float, default=0.10)
    parser.add_argument("--horizon", type=int, action="append", default=[12, 36])
    args = parser.parse_args()
    scenarios = json.loads(args.fixture.read_text(encoding="utf-8"))
    print(json.dumps({name: calculate(value, args.horizon, args.rate) for name, value in scenarios.items()}, indent=2))


if __name__ == "__main__":
    main()
