"""Command-line interface for the offline starter kit."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from .evals import evaluate_query
from .packs import PackError, discover_packs, load_pack
from .validation import run_named_query, validate_pack as validate_pack_data

app = typer.Typer(help="Build and validate ontology example packs.")


def _examples_root() -> Path:
    candidates = (Path.cwd() / "examples", Path(__file__).resolve().parents[2] / "examples")
    return next((candidate for candidate in candidates if candidate.is_dir()), candidates[0])


@app.command("packs")
def list_packs() -> None:
    """List bundled packs as JSON."""
    typer.echo(json.dumps({key: pack.manifest.get("title", key) for key, pack in discover_packs(_examples_root()).items()}, indent=2))


@app.command("validate")
def validate_pack(pack_path: Path) -> None:
    """Validate an example pack's manifest paths and SHACL data."""
    try:
        pack = load_pack(pack_path)
    except PackError as exc:
        raise typer.BadParameter(str(exc)) from exc
    report = validate_pack_data(pack)
    typer.echo(json.dumps({"id": pack.pack_id, "status": "valid" if report.conforms else "invalid", "messages": list(report.messages)}))
    if not report.conforms:
        raise typer.Exit(code=1)


@app.command("query")
def query_pack(pack_path: Path, query_id: str) -> None:
    """Run a named competency question from a pack."""
    try:
        pack = load_pack(pack_path)
        rows = run_named_query(pack, query_id)
    except PackError as exc:
        raise typer.BadParameter(str(exc)) from exc
    typer.echo(json.dumps(rows, indent=2))


@app.command("eval")
def eval_pack(pack_path: Path, query_id: str) -> None:
    """Evaluate a named query against its expected fixture."""
    try:
        result = evaluate_query(load_pack(pack_path), query_id)
    except PackError as exc:
        raise typer.BadParameter(str(exc)) from exc
    typer.echo(json.dumps(result, indent=2))
    if not bool(result["passed"]):
        raise typer.Exit(code=1)


def main() -> None:
    app()
