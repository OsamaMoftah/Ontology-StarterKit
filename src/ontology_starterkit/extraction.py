"""Deterministic building blocks for ontology-guided extraction lessons.

The starter kit deliberately keeps model calls out of the core. These helpers
make the contract explicit so a hosted extractor can be added later without
silently inventing entities or identifiers.
"""

from __future__ import annotations

import unicodedata
from collections.abc import Iterable, Mapping


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
