"""Deterministic LinkML schema scaffolding for reviewed ontology slices."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from typing import cast

import yaml


_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def build_linkml_schema(
    name: str,
    classes: Mapping[str, Iterable[str]],
    *,
    schema_id: str = "https://ontology-starterkit.dev/schema",
    slot_specs: Mapping[str, Mapping[str, object]] | None = None,
) -> str:
    """Render a reviewed class-to-slot mapping as LinkML YAML.

    ``slot_specs`` supports reviewed cardinalities, enums, and identifiers.
    Unsupported LinkML constructs are intentionally left out of this adapter.
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
    specs = slot_specs or {}
    undeclared = sorted(set(specs) - slots)
    if undeclared:
        raise ValueError(f"slot_specs contains undeclared slot(s): {', '.join(undeclared)}")
    rendered_slots: dict[str, dict[str, object]] = {}
    for slot in sorted(slots):
        spec = dict(specs.get(slot, {}))
        rendered: dict[str, object] = {"range": str(spec.pop("range", "string"))}
        required_supplied = "required" in spec
        if "required" in spec:
            rendered["required"] = bool(spec.pop("required"))
        if "identifier" in spec:
            rendered["identifier"] = bool(spec.pop("identifier"))
        minimum = _cardinality(spec.pop("minimum_cardinality"), slot, "minimum") if "minimum_cardinality" in spec else None
        maximum = _cardinality(spec.pop("maximum_cardinality"), slot, "maximum") if "maximum_cardinality" in spec else None
        if minimum is not None and maximum is not None and minimum > maximum:
            raise ValueError(f"minimum cardinality cannot exceed maximum for {slot}")
        if minimum is not None:
            rendered["minimum_cardinality"] = minimum
        if maximum is not None:
            rendered["maximum_cardinality"] = maximum
        if minimum is not None or maximum is not None:
            if maximum is None or maximum != 1:
                rendered["multivalued"] = True
            if minimum is not None and minimum > 0 and not required_supplied:
                rendered["required"] = True
        if "enum" in spec:
            enum_values = cast(object, spec.pop("enum"))
            if not isinstance(enum_values, (list, tuple)) or not enum_values:
                raise ValueError(f"enum for {slot} must be a non-empty list")
            enum_name = f"{slot.title()}Enum"
            rendered["range"] = enum_name
        if spec:
            raise ValueError(f"unsupported LinkML slot options for {slot}: {sorted(spec)}")
        rendered_slots[slot] = rendered
    enums: dict[str, dict[str, object]] = {}
    for slot, slot_spec in specs.items():
        if "enum" in slot_spec:
            enum_values = cast(list[object] | tuple[object, ...], slot_spec["enum"])
            enums[f"{slot.title()}Enum"] = {"permissible_values": {str(value): {} for value in enum_values}}
    payload: dict[str, object] = {
        "id": schema_id,
        "name": name,
        "prefixes": {"linkml": "https://w3id.org/linkml/", "local": schema_id.rstrip("/#") + "/"},
        "imports": ["linkml:types"],
        "default_prefix": "local",
        "classes": rendered_classes,
        "slots": rendered_slots,
    }
    if enums:
        payload["enums"] = enums
    return yaml.safe_dump(payload, sort_keys=False)


def _cardinality(value: object, slot: str, bound: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{bound} cardinality for {slot} must be a non-negative integer")
    return value
