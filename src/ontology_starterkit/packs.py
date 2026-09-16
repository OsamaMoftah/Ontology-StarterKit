"""Pack discovery and safe manifest loading."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import re

import yaml


_SUPPORTED_MANIFEST_VERSION = re.compile(r"^0\.\d+\.\d+$")
_REQUIRED_FIELDS = ("id", "title", "version", "ontology", "shapes", "data", "questions", "queries", "expected", "sources", "diagram", "license")


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
    Pack(root, {}).resolve("manifest.yaml")
    try:
        manifest = yaml.safe_load(manifest_path.read_text()) or {}
    except yaml.YAMLError as exc:
        raise PackError(f"invalid manifest YAML: {manifest_path}") from exc
    if not isinstance(manifest, dict):
        raise PackError("manifest must be a mapping")
    if not isinstance(manifest["id"], str) or not re.fullmatch(r"[a-z0-9][a-z0-9-]+", manifest["id"]):
        raise PackError("manifest id must be a lowercase kebab-case string")
    if "version" in manifest and (not isinstance(manifest["version"], str) or not _SUPPORTED_MANIFEST_VERSION.fullmatch(manifest["version"])):
        raise PackError("manifest version is unsupported; use a 0.x.y version")
    for field in ("ontology", "shapes", "questions", "data", "sources", "diagram"):
        value = manifest.get(field)
        if value:
            if not isinstance(value, str):
                raise PackError(f"manifest field must be a string: {field}")
            Pack(root, manifest).resolve(value)
    missing = [field for field in _REQUIRED_FIELDS if not manifest.get(field)]
    if missing:
        raise PackError(f"manifest requires fields: {', '.join(missing)}")
    for field in ("queries", "expected"):
        values = manifest.get(field, {})
        if not isinstance(values, dict):
            raise PackError(f"manifest field must be a mapping: {field}")
        for query_id, value in values.items():
            if not isinstance(query_id, str) or not isinstance(value, str):
                raise PackError(f"manifest {field} entries must be string pairs")
            Pack(root, manifest).resolve(value)
    query_ids = set(manifest["queries"])
    expected_ids = set(manifest["expected"])
    if query_ids != expected_ids:
        raise PackError(f"query/expected IDs differ; missing expected={sorted(query_ids - expected_ids)}")
    try:
        questions = yaml.safe_load(Pack(root, manifest).resolve(str(manifest["questions"])).read_text()) or []
    except yaml.YAMLError as exc:
        raise PackError("questions file is not valid YAML") from exc
    if not isinstance(questions, list) or not all(isinstance(item, dict) and item.get("id") and item.get("query") for item in questions):
        raise PackError("questions must be a list of records with id and query")
    if {str(item["id"]) for item in questions} != query_ids:
        raise PackError("questions IDs must match manifest query IDs")
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
            if child.resolve().parent != root.resolve():
                raise PackError(f"pack path is outside the configured examples root: {child}")
            pack = load_pack(child)
            if pack.pack_id in packs:
                raise PackError(f"duplicate pack id: {pack.pack_id}")
            packs[pack.pack_id] = pack
    return packs
