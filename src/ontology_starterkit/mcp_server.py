"""Optional, bounded MCP adapter for local ontology packs.

The pure tool functions are useful in tests and documentation even when the
optional ``mcp`` dependency is not installed. No tool accepts arbitrary
SPARQL; queries must be declared in a pack manifest.
"""

from __future__ import annotations

import json
import multiprocessing
from pathlib import Path
import time
from typing import Any

from .packs import Pack, PackError, discover_packs, load_pack
from .validation import run_named_query, validate_pack


def _query_worker(pack_path: str, query_id: str, result_queue: Any, delay_seconds: float) -> None:
    """Run one query in a disposable process and send only JSON-safe data back."""
    try:
        if delay_seconds:
            time.sleep(delay_seconds)
        pack = load_pack(pack_path)
        result_queue.put(("ok", run_named_query(pack, query_id)))
    except Exception as exc:  # pragma: no cover - exercised through the parent boundary
        result_queue.put(("error", str(exc)))


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


def _limit(value: int, *, name: str, maximum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise PackError(f"{name} must be an integer between 1 and {maximum}")
    return value


def run_query_tool(
    pack_path: str | Path,
    query_id: str,
    *,
    examples_root: str | Path | None = None,
    max_rows: int = 100,
    max_bytes: int = 64_000,
    timeout_seconds: float = 5.0,
    _worker_delay_seconds: float = 0.0,
) -> dict[str, Any]:
    """Run one declared query with bounded local execution and output.

    The worker is a disposable process and is terminated on timeout. This
    prevents an expensive local query from occupying the MCP server after its
    deadline; a database adapter must additionally use a database transaction
    timeout and verify server-side cancellation. ``_worker_delay_seconds`` is
    private and exists only for the isolation benchmark.
    """
    pack: Pack = load_pack(_bounded_pack_path(pack_path, examples_root))
    max_rows = _limit(max_rows, name="max_rows", maximum=10_000)
    max_bytes = _limit(max_bytes, name="max_bytes", maximum=10_000_000)
    if isinstance(timeout_seconds, bool) or not isinstance(timeout_seconds, (int, float)) or not 0 < timeout_seconds <= 60:
        raise PackError("timeout_seconds must be a number between 0 and 60")
    if isinstance(_worker_delay_seconds, bool) or not isinstance(_worker_delay_seconds, (int, float)) or not 0 <= _worker_delay_seconds <= 60:
        raise PackError("_worker_delay_seconds must be a number between 0 and 60")
    context = multiprocessing.get_context("spawn")
    result_queue = context.Queue(maxsize=1)
    process = context.Process(
        target=_query_worker,
        args=(str(pack.root), query_id, result_queue, float(_worker_delay_seconds)),
        name="ontokit-mcp-query",
        daemon=True,
    )
    process.start()
    process.join(timeout=float(timeout_seconds))
    try:
        if process.is_alive():
            process.terminate()
            process.join(timeout=2)
            raise PackError("named query exceeded its MCP deadline")
        if process.exitcode not in (0, None):
            raise PackError(f"named query worker exited with code {process.exitcode}")
        try:
            kind, payload = result_queue.get(timeout=1)
        except Exception as exc:
            raise PackError("named query worker returned no result") from exc
        if kind == "error":
            raise PackError(str(payload))
        rows = payload
    finally:
        result_queue.close()
        result_queue.join_thread()
        if process.is_alive():
            process.terminate()
            process.join(timeout=2)
    if len(rows) > max_rows:
        raise PackError(f"named query returned more than {max_rows} rows")
    encoded = json.dumps(rows, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if len(encoded) > max_bytes:
        raise PackError(f"named query response exceeds {max_bytes} bytes")
    return {
        "pack": pack.pack_id,
        "query": query_id,
        "rows": rows,
        "limits": {"max_rows": max_rows, "max_bytes": max_bytes, "worker": "process"},
    }


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
    def query(
        pack_path: str,
        query_id: str,
        max_rows: int = 100,
        max_bytes: int = 64_000,
        timeout_seconds: float = 5.0,
    ) -> dict[str, Any]:
        return run_query_tool(
            pack_path,
            query_id,
            examples_root=examples_root,
            max_rows=max_rows,
            max_bytes=max_bytes,
            timeout_seconds=timeout_seconds,
        )

    server.run(transport="stdio")
