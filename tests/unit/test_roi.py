from ontology_starterkit.roi import Scenario, npv, payback_months, roi_percent


def test_roi_example_and_zero_rate_npv():
    scenario = Scenario(3, 15000, 5000, 2000, 4000, (8000, 10000, 3000, 15000))
    assert scenario.upfront_cost == 60000
    assert scenario.net_monthly_benefit == 30000
    assert payback_months(scenario) == 2
    assert round(npv(scenario, 12, 0), 2) == 300000
    assert round(roi_percent(scenario, 12), 1) == 227.3


def test_roi_reports_no_payback_for_negative_benefit():
    scenario = Scenario(1, 100, 0, 100, 100, (0,))
    assert payback_months(scenario) is None
