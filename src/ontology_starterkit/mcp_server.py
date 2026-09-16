"""Optional, bounded MCP adapter for local ontology packs.

The pure tool functions are useful in tests and documentation even when the
optional ``mcp`` dependency is not installed. No tool accepts arbitrary
SPARQL; queries must be declared in a pack manifest.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .packs import Pack, discover_packs, load_pack
from .validation import run_named_query, validate_pack


def list_pack_tools(examples_root: str | Path) -> list[dict[str, str]]:
    """Describe the safe tools exposed for each local pack."""
    return [
        {"pack": pack.pack_id, "query": query_id}
        for pack in discover_packs(examples_root).values()
        for query_id in pack.manifest.get("queries", {})
    ]


def validate_pack_tool(pack_path: str | Path) -> dict[str, object]:
    pack = load_pack(pack_path)
    report = validate_pack(pack)
    return {"pack": pack.pack_id, "conforms": report.conforms, "messages": list(report.messages)}


def run_query_tool(pack_path: str | Path, query_id: str) -> dict[str, Any]:
    pack: Pack = load_pack(pack_path)
    return {"pack": pack.pack_id, "query": query_id, "rows": run_named_query(pack, query_id)}


def serve(examples_root: str | Path) -> None:
    """Run a stdio MCP server when the optional dependency is installed."""
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError as exc:  # pragma: no cover - exercised by installation docs
        raise RuntimeError("install ontology-starterkit[mcp] to run the MCP adapter") from exc

    server = FastMCP("ontology-starterkit")

    @server.tool()
    def list_packs() -> list[dict[str, str]]:
        return list_pack_tools(examples_root)

    @server.tool()
    def validate(pack_path: str) -> dict[str, object]:
        return validate_pack_tool(pack_path)

    @server.tool()
    def query(pack_path: str, query_id: str) -> dict[str, Any]:
        return run_query_tool(pack_path, query_id)

    server.run(transport="stdio")

