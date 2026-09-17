"""Deterministic building blocks for ontology-guided extraction lessons.

The starter kit deliberately keeps model calls out of the core. These helpers
make the contract explicit so a hosted extractor can be added later without
silently inventing entities or identifiers.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import asdict, dataclass
from collections.abc import Iterable, Mapping


@dataclass(frozen=True)
class ExtractionCandidate:
    text: str
    start: int
    end: int
    class_id: str
    source_id: str
    model: str
    confidence: float

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


def extract_candidates(source: str, allowed_terms: Mapping[str, str], *, source_id: str, model: str = "deterministic-rule-v1") -> list[ExtractionCandidate]:
    """Extract exact mentions from a reviewed vocabulary without inference."""
    candidates: list[ExtractionCandidate] = []
    for phrase, class_id in sorted(allowed_terms.items(), key=lambda item: (-len(item[0]), item[0])):
        for match in re.finditer(re.escape(phrase), source, re.IGNORECASE):
            candidates.append(ExtractionCandidate(match.group(0), match.start(), match.end(), class_id, source_id, model, 1.0))
    return sorted(candidates, key=lambda item: (item.start, item.end, item.class_id))


def validate_candidates(source: str, candidates: Iterable[ExtractionCandidate], allowed_classes: set[str]) -> list[str]:
    """Return validation errors for class IDs, exact spans, and confidence."""
    errors: list[str] = []
    for candidate in candidates:
        if candidate.class_id not in allowed_classes:
            errors.append(f"unsupported class: {candidate.class_id}")
        if not (0 <= candidate.start < candidate.end <= len(source)) or source[candidate.start:candidate.end] != candidate.text:
            errors.append(f"invalid source span for: {candidate.text}")
        if not 0 <= candidate.confidence <= 1:
            errors.append(f"invalid confidence for: {candidate.text}")
    return errors


def normalize_identifier(value: str) -> str:
    """Create a stable comparison key for a human-entered identifier."""
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(
        "".join(character if (character.isalnum() or character == "_") else " " for character in normalized).split()
    )


def _reviewed_aliases(aliases: Mapping[str, str]) -> dict[str, str]:
    reviewed: dict[str, str] = {}
    for alias, canonical in aliases.items():
        key = normalize_identifier(alias)
        previous = reviewed.get(key)
        if previous is not None and previous != canonical:
            raise ValueError(f"alias collision for {alias!r}: {previous!r} and {canonical!r}")
        reviewed[key] = canonical
    return reviewed


def resolve_aliases(
    records: Iterable[Mapping[str, str]], aliases: Mapping[str, str], *, fields: set[str] | None = None
) -> list[dict[str, str]]:
    """Apply a reviewed alias table without merging ambiguous values."""
    reviewed = _reviewed_aliases(aliases)
    resolved: list[dict[str, str]] = []
    for record in records:
        item = dict(record)
        for key, value in tuple(item.items()):
            if fields is None or key in fields:
                item[key] = reviewed.get(normalize_identifier(value), value)
        resolved.append(item)
    return resolved


def resolve_aliases_with_audit(
    records: Iterable[Mapping[str, str]], aliases: Mapping[str, str], *, fields: set[str] | None = None
) -> list[dict[str, object]]:
    """Resolve reviewed aliases and retain field-level provenance for every change."""
    reviewed = _reviewed_aliases(aliases)
    audited: list[dict[str, object]] = []
    for record in records:
        item = dict(record)
        changes: list[dict[str, str]] = []
        for key, value in tuple(item.items()):
            if fields is not None and key not in fields:
                continue
            canonical = reviewed.get(normalize_identifier(value))
            if canonical is not None and canonical != value:
                item[key] = canonical
                changes.append({"field": key, "original": value, "canonical": canonical})
        audited.append({"record": item, "changes": changes})
    return audited


def extraction_contract(terms: Iterable[str]) -> dict[str, object]:
    """Return a model-independent extraction contract for an ontology slice."""
    normalized = tuple(dict.fromkeys(term.strip() for term in terms if term.strip()))
    return {
        "terms": normalized,
        "require_source_span": True,
        "require_confidence": True,
        "allow_new_classes": False,
        "abstain_on_ambiguity": True,
    }
