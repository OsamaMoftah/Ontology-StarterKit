"""Optional, bounded MCP adapter for local ontology packs.

The pure tool functions are useful in tests and documentation even when the
optional ``mcp`` dependency is not installed. No tool accepts arbitrary
SPARQL; queries must be declared in a pack manifest.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .packs import Pack, PackError, discover_packs, load_pack
from .validation import run_named_query, validate_pack


def list_pack_tools(examples_root: str | Path) -> list[dict[str, str]]:
    """Describe the safe tools exposed for each local pack."""
    return [
        {"pack": pack.pack_id, "query": query_id}
        for pack in discover_packs(examples_root).values()
        for query_id in pack.manifest.get("queries", {})
    ]


def _bounded_pack_path(pack_path: str | Path, examples_root: str | Path | None) -> Path:
    candidate = Path(pack_path).resolve()
    if examples_root is not None:
        root = Path(examples_root).resolve()
        if not Path(pack_path).is_absolute():
            candidate = (root / pack_path).resolve()
        try:
            relative = candidate.relative_to(root)
        except ValueError as exc:
            raise PackError("pack path is outside the configured examples root") from exc
        if len(relative.parts) != 1:
            raise PackError("pack path must be an immediate child of the configured examples root")
    return candidate


def validate_pack_tool(pack_path: str | Path, *, examples_root: str | Path | None = None) -> dict[str, object]:
    pack = load_pack(_bounded_pack_path(pack_path, examples_root))
    report = validate_pack(pack)
    return {"pack": pack.pack_id, "conforms": report.conforms, "messages": list(report.messages)}


def run_query_tool(pack_path: str | Path, query_id: str, *, examples_root: str | Path | None = None) -> dict[str, Any]:
    pack: Pack = load_pack(_bounded_pack_path(pack_path, examples_root))
    return {"pack": pack.pack_id, "query": query_id, "rows": run_named_query(pack, query_id)}


def serve(examples_root: str | Path) -> None:
    """Run a stdio MCP server when the optional dependency is installed."""
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover - exercised by installation docs
        raise RuntimeError("install ontology-starterkit[mcp] to run the MCP adapter") from exc

    server = FastMCP("ontology-starterkit")
    examples_root = Path(examples_root).resolve()

    @server.tool()
    def list_packs() -> list[dict[str, str]]:
        return list_pack_tools(examples_root)

    @server.tool()
    def validate(pack_path: str) -> dict[str, object]:
        return validate_pack_tool(pack_path, examples_root=examples_root)

    @server.tool()
    def query(pack_path: str, query_id: str) -> dict[str, Any]:
        return run_query_tool(pack_path, query_id, examples_root=examples_root)

    server.run(transport="stdio")
