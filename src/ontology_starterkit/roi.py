"""Executable ROI scenarios for the ontology investment worksheet."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    build_months: int
    engineering_monthly: float
    sme_monthly: float
    infrastructure_monthly: float
    maintenance_monthly: float
    monthly_benefits: tuple[float, ...]

    def __post_init__(self) -> None:
        values = (self.build_months, self.engineering_monthly, self.sme_monthly, self.infrastructure_monthly, self.maintenance_monthly, *self.monthly_benefits)
        if self.build_months <= 0 or any(value < 0 for value in values):
            raise ValueError("scenario values must be non-negative and build_months must be positive")

    @property
    def upfront_cost(self) -> float:
        return (self.engineering_monthly + self.sme_monthly) * self.build_months

    @property
    def ongoing_cost(self) -> float:
        return self.infrastructure_monthly + self.maintenance_monthly

    @property
    def monthly_value(self) -> float:
        return sum(self.monthly_benefits)

    @property
    def net_monthly_benefit(self) -> float:
        return self.monthly_value - self.ongoing_cost


def payback_months(scenario: Scenario) -> float | None:
    """Return payback from launch, or ``None`` when assumptions never pay back."""
    if scenario.net_monthly_benefit <= 0:
        return None
    return scenario.upfront_cost / scenario.net_monthly_benefit


def npv(scenario: Scenario, months: int, annual_discount_rate: float) -> float:
    if months <= 0 or annual_discount_rate < 0:
        raise ValueError("months must be positive and discount rate non-negative")
    if annual_discount_rate == 0:
        return -scenario.upfront_cost + scenario.net_monthly_benefit * months
    monthly_rate = (1 + annual_discount_rate) ** (1 / 12) - 1
    return -scenario.upfront_cost + scenario.net_monthly_benefit * (1 - (1 + monthly_rate) ** -months) / monthly_rate


def roi_percent(scenario: Scenario, months: int) -> float:
    if months <= 0:
        raise ValueError("months must be positive")
    investment = scenario.upfront_cost + scenario.ongoing_cost * months
    if investment == 0:
        return 0.0
    return ((scenario.monthly_value * months - investment) / investment) * 100
