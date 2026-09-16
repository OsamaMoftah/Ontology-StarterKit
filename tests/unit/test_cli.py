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


def test_cli_validation_and_eval_fail_with_nonzero_status(tmp_path):
    invalid_pack = tmp_path / "hello-ontology"
    import shutil
    shutil.copytree(ROOT / "examples/hello-ontology", invalid_pack)
    (invalid_pack / "data.ttl").write_text((invalid_pack / "data/valid.ttl").read_text())
    invalid_pack.joinpath("manifest.yaml").write_text(
        (invalid_pack / "manifest.yaml").read_text().replace("data/valid.ttl", "data/invalid/missing-name.ttl")
    )
    validated = runner.invoke(app, ["validate", str(invalid_pack)])
    assert validated.exit_code != 0

    expected = invalid_pack / "expected/manager.json"
    expected.write_text('[{"person": "https://ontology-starterkit.dev/hello/maya", "personName": "Maya Chen"}]')
    evaluated = runner.invoke(app, ["eval", str(invalid_pack), "manager"])
    assert evaluated.exit_code != 0
