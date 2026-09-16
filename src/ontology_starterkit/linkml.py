"""Deterministic LinkML schema scaffolding for reviewed ontology slices."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping

import yaml


_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def build_linkml_schema(
    name: str,
    classes: Mapping[str, Iterable[str]],
    *,
    schema_id: str = "https://ontology-starterkit.dev/schema",
) -> str:
    """Render a reviewed class-to-slot mapping as LinkML YAML.

    This is scaffolding: cardinalities, enums and semantic mappings still need
    domain review before the schema is used for data generation or validation.
    """
    if not name.strip() or not schema_id.strip():
        raise ValueError("name and schema_id are required")
    rendered_classes: dict[str, dict[str, list[str]]] = {}
    slots: set[str] = set()
    for class_name, class_slots in classes.items():
        if not _IDENTIFIER.fullmatch(class_name):
            raise ValueError(f"invalid class identifier: {class_name}")
        values = list(dict.fromkeys(slot.strip() for slot in class_slots if slot.strip()))
        if any(not _IDENTIFIER.fullmatch(slot) for slot in values):
            raise ValueError(f"invalid slot identifier for {class_name}")
        rendered_classes[class_name] = {"slots": values}
        slots.update(values)
    payload = {
        "id": schema_id,
        "name": name,
        "prefixes": {"linkml": "https://w3id.org/linkml/", "local": schema_id.rstrip("/#") + "/"},
        "imports": ["linkml:types"],
        "default_prefix": "local",
        "classes": rendered_classes,
        "slots": {slot: {"range": "string"} for slot in sorted(slots)},
    }
    return yaml.safe_dump(payload, sort_keys=False)
