import json
from pathlib import Path

from typer.testing import CliRunner

from ontology_starterkit.cli import app


ROOT = Path(__file__).resolve().parents[2]
runner = CliRunner()


def test_cli_lists_packs():
    result = runner.invoke(app, ["packs"])
    assert result.exit_code == 0
    assert "hello-ontology" in result.stdout


def test_cli_validates_and_queries_pack():
    path = str(ROOT / "examples/hello-ontology")
    validated = runner.invoke(app, ["validate", path])
    assert validated.exit_code == 0
    assert json.loads(validated.stdout)["status"] == "valid"
    queried = runner.invoke(app, ["query", path, "manager"])
    assert queried.exit_code == 0
    assert "Maya Chen" in queried.stdout


def test_cli_evaluates_pack():
    result = runner.invoke(app, ["eval", str(ROOT / "examples/hello-ontology"), "manager"])
    assert result.exit_code == 0
    assert json.loads(result.stdout)["passed"] is True

