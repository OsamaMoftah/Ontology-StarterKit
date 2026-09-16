"""Deterministic building blocks for ontology-guided extraction lessons.

The starter kit deliberately keeps model calls out of the core. These helpers
make the contract explicit so a hosted extractor can be added later without
silently inventing entities or identifiers.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping


def normalize_identifier(value: str) -> str:
    """Create a stable comparison key for a human-entered identifier."""
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def resolve_aliases(
    records: Iterable[Mapping[str, str]], aliases: Mapping[str, str]
) -> list[dict[str, str]]:
    """Apply a reviewed alias table without merging ambiguous values."""
    reviewed = {normalize_identifier(alias): canonical for alias, canonical in aliases.items()}
    resolved: list[dict[str, str]] = []
    for record in records:
        item = dict(record)
        for key, value in tuple(item.items()):
            item[key] = reviewed.get(normalize_identifier(value), value)
        resolved.append(item)
    return resolved


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

