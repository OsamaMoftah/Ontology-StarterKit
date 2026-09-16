"""Reviewable, reversible identity mapping for ontology examples.

Names are candidate evidence, never proof of identity. A mapping is applied
only after an explicit decision record is approved.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import date
from typing import Iterable, Mapping

from .extraction import normalize_identifier


@dataclass(frozen=True)
class MappingDecision:
    source_id: str
    field: str
    original: str
    canonical: str | None
    status: str
    reviewer: str | None
    decided_at: str | None
    mapping_version: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def review_alias_candidates(
    records: Iterable[Mapping[str, str]], aliases: Mapping[str, str], *, field: str, mapping_version: str
) -> list[MappingDecision]:
    """Create approved, rejected, or queued decisions without mutating records."""
    indexed: dict[str, set[str]] = {}
    for alias, canonical in aliases.items():
        indexed.setdefault(normalize_identifier(alias), set()).add(canonical)
    decisions: list[MappingDecision] = []
    for record in records:
        original = str(record.get(field, ""))
        choices = indexed.get(normalize_identifier(original), set())
        if len(choices) == 1:
            canonical = next(iter(choices))
            decisions.append(MappingDecision(str(record.get("id", "")), field, original, canonical, "queued", None, None, mapping_version))
        else:
            decisions.append(MappingDecision(str(record.get("id", "")), field, original, None, "ambiguous" if choices else "unmatched", None, None, mapping_version))
    return decisions


def approve_decision(decision: MappingDecision, reviewer: str, *, approved_on: str | None = None) -> MappingDecision:
    """Approve a queued unique mapping, preserving the reviewer and date."""
    if decision.status != "queued" or not decision.canonical:
        raise ValueError("only queued decisions with one canonical target can be approved")
    return MappingDecision(
        source_id=decision.source_id,
        field=decision.field,
        original=decision.original,
        canonical=decision.canonical,
        status="approved",
        reviewer=reviewer,
        decided_at=approved_on or date.today().isoformat(),
        mapping_version=decision.mapping_version,
    )


def apply_decisions(records: Iterable[Mapping[str, str]], decisions: Iterable[MappingDecision]) -> list[dict[str, str]]:
    """Apply approved decisions idempotently; leave all other records unchanged."""
    approved = {(d.source_id, d.field): d for d in decisions if d.status == "approved"}
    result: list[dict[str, str]] = []
    for record in records:
        item = dict(record)
        for (source_id, field), decision in approved.items():
            if str(item.get("id", "")) == source_id and field in item and item[field] == decision.original:
                item[field] = str(decision.canonical)
        result.append(item)
    return result


def rollback_decisions(records: Iterable[Mapping[str, str]], decisions: Iterable[MappingDecision]) -> list[dict[str, str]]:
    """Reverse approved mappings only when the current value is the mapped target."""
    approved = {(d.source_id, d.field): d for d in decisions if d.status == "approved"}
    result: list[dict[str, str]] = []
    for record in records:
        item = dict(record)
        for (source_id, field), decision in approved.items():
            if str(item.get("id", "")) == source_id and item.get(field) == decision.canonical:
                item[field] = decision.original
        result.append(item)
    return result
