"""Pack discovery and safe manifest loading."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


class PackError(ValueError):
    """Raised when an example pack is missing or malformed."""


@dataclass(frozen=True)
class Pack:
    """A validated example-pack directory."""

    root: Path
    manifest: dict[str, Any]

    @property
    def pack_id(self) -> str:
        return str(self.manifest["id"])

    def resolve(self, relative: str) -> Path:
        """Resolve a manifest path without permitting traversal."""
        candidate = (self.root / relative).resolve()
        try:
            candidate.relative_to(self.root.resolve())
        except ValueError as exc:
            raise PackError(f"manifest path escapes pack: {relative}") from exc
        if not candidate.exists():
            raise PackError(f"manifest path does not exist: {relative}")
        return candidate


def load_pack(path: str | Path) -> Pack:
    """Load and minimally validate a pack manifest."""
    root = Path(path).resolve()
    manifest_path = root / "manifest.yaml"
    if not manifest_path.is_file():
        raise PackError(f"pack requires manifest.yaml: {root}")
    try:
        manifest = yaml.safe_load(manifest_path.read_text()) or {}
    except yaml.YAMLError as exc:
        raise PackError(f"invalid manifest YAML: {manifest_path}") from exc
    if not isinstance(manifest, dict) or not manifest.get("id"):
        raise PackError("manifest requires a non-empty id")
    for field in ("ontology", "shapes", "questions", "data", "sources", "diagram"):
        value = manifest.get(field)
        if value:
            if not isinstance(value, str):
                raise PackError(f"manifest field must be a string: {field}")
            Pack(root, manifest).resolve(value)
    for field in ("queries", "expected"):
        values = manifest.get(field, {})
        if not isinstance(values, dict):
            raise PackError(f"manifest field must be a mapping: {field}")
        for query_id, value in values.items():
            if not isinstance(query_id, str) or not isinstance(value, str):
                raise PackError(f"manifest {field} entries must be string pairs")
            Pack(root, manifest).resolve(value)
    invalid = manifest.get("invalid", [])
    if not isinstance(invalid, list) or not all(isinstance(value, str) for value in invalid):
        raise PackError("manifest field must be a list of paths: invalid")
    for value in invalid:
        Pack(root, manifest).resolve(value)
    return Pack(root=root, manifest=manifest)


def discover_packs(examples_root: str | Path) -> dict[str, Pack]:
    """Discover immediate child directories that contain valid manifests."""
    root = Path(examples_root)
    packs: dict[str, Pack] = {}
    if not root.is_dir():
        return packs
    for child in sorted(root.iterdir()):
        if child.is_dir() and (child / "manifest.yaml").is_file():
            pack = load_pack(child)
            if pack.pack_id in packs:
                raise PackError(f"duplicate pack id: {pack.pack_id}")
            packs[pack.pack_id] = pack
    return packs
