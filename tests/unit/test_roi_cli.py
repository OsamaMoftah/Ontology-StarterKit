import json
from pathlib import Path

from scripts.calculate_roi import calculate


ROOT = Path(__file__).resolve().parents[2]


def test_roi_cli_reproduces_worked_example_and_no_payback():
    scenarios = json.loads((ROOT / "docs/for-product-managers/roi-calculator/scenarios.json").read_text())
    base = calculate(scenarios["base"], [12, 36], 0.10)
    assert base["upfront_cost"] == 60000
    assert round(base["payback_months"], 1) == 2.0
    assert round(base["horizons"]["12"]["roi_percent"], 1) == 227.3
    assert calculate(scenarios["no_payback"], [12], 0)["payback_months"] is None
