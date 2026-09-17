# ROI Calculator

Build a business case for investing in an ontology or knowledge graph. This folder has formulas, a worked example, and a template.

## What It Includes

- [ROI template](roi-template.md): formulas for costs, savings, ROI, NPV, and payback period.
- [Investment one-pager](../investment-one-pager.md): a concise executive summary template.
- [`scenarios.json`](scenarios.json) and [`scripts/calculate_roi.py`](../../../scripts/calculate_roi.py): executable hypothetical scenarios with sensitivity horizons.

## Recommended Workflow

1. Estimate build and maintenance costs with engineering and domain leads.
2. Quantify current pain from hallucinations, manual reconciliation, and delayed feature delivery.
3. Fill in the ROI template with a 12- or 36-month horizon.
4. Convert the result into the investment one-pager for leadership review.

## Important Caveat

The numbers in this folder are examples. Replace them with your own product, team, and risk data before sharing them.

Reproduce the worked example with `python scripts/calculate_roi.py docs/for-product-managers/roi-calculator/scenarios.json --rate 0.10`. The calculator rejects duplicate benefit labels, invalid inputs, and inconsistent horizons; its output is illustrative until an owner replaces the assumptions with measured operating data.
