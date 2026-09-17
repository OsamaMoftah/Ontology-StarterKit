from pathlib import Path

import pytest

from ontology_starterkit.packs import PackError, discover_packs, load_pack


ROOT = Path(__file__).resolve().parents[2]


def test_discover_packs_includes_hello_pack():
    packs = discover_packs(ROOT / "examples")
    assert "hello-ontology" in packs


def test_load_pack_requires_manifest(tmp_path):
    (tmp_path / "broken").mkdir()
    with pytest.raises(PackError, match="manifest.yaml"):
        load_pack(tmp_path / "broken")


def test_load_pack_reports_missing_required_id(tmp_path):
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "manifest.yaml").write_text("version: 0.2.0\n")
    with pytest.raises(PackError, match="manifest requires fields: id"):
        load_pack(pack)


def test_load_pack_rejects_path_escape(tmp_path):
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "manifest.yaml").write_text("id: demo\nontology: ../outside.ttl\n")
    with pytest.raises(PackError, match="path"):
        load_pack(pack)


def test_load_pack_rejects_non_string_manifest_path(tmp_path):
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "manifest.yaml").write_text("id: demo\nontology: [ontology.ttl]\n")
    with pytest.raises(PackError, match="field must be a string: ontology"):
        load_pack(pack)


def test_load_pack_requires_supported_version(tmp_path):
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "manifest.yaml").write_text(
        "id: demo\nversion: 9.0.0\nontology: ontology.ttl\nshapes: shapes.ttl\ndata: data.ttl\n"
        "questions: questions.yaml\nqueries: {one: queries/one.rq}\nexpected: {one: expected/one.json}\n"
    )
    for name in ("ontology.ttl", "shapes.ttl", "data.ttl", "questions.yaml"):
        (pack / name).write_text("")
    (pack / "queries").mkdir()
    (pack / "expected").mkdir()
    (pack / "queries/one.rq").write_text("SELECT * WHERE { ?s ?p ?o }")
    (pack / "expected/one.json").write_text("[]")
    with pytest.raises(PackError, match="version"):
        load_pack(pack)


def test_load_pack_rejects_query_without_expected_fixture(tmp_path):
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "manifest.yaml").write_text(
        "id: demo\nversion: 0.2.0\nontology: ontology.ttl\nshapes: shapes.ttl\ndata: data.ttl\n"
        "questions: questions.yaml\nqueries: {one: queries/one.rq}\nexpected: {}\n"
    )
    for name in ("ontology.ttl", "shapes.ttl", "data.ttl", "questions.yaml"):
        (pack / name).write_text("")
    (pack / "queries").mkdir()
    (pack / "queries/one.rq").write_text("SELECT * WHERE { ?s ?p ?o }")
    with pytest.raises(PackError, match="expected"):
        load_pack(pack)


def test_load_pack_reports_both_query_fixture_mismatch_directions(tmp_path):
    import shutil
    import yaml

    pack = tmp_path / "hello"
    shutil.copytree(ROOT / "examples/hello-ontology", pack)
    manifest_path = pack / "manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text())
    manifest["expected"]["extra"] = manifest["expected"]["manager"]
    manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False))
    with pytest.raises(PackError, match=r"missing expected=\[\].*missing query=\['extra'\]"):
        load_pack(pack)


def test_validate_pack_rejects_unrelated_graph(tmp_path):
    from ontology_starterkit.validation import validate_pack

    source = ROOT / "examples/hello-ontology"
    pack = tmp_path / "hello"
    import shutil
    shutil.copytree(source, pack)
    data = pack / "data/unrelated.ttl"
    data.write_text("@prefix ex: <urn:other:> . ex:x ex:p ex:y .\n")
    report = validate_pack(load_pack(pack), data_path="data/unrelated.ttl")
    assert report.conforms is False
    assert any("target" in message.lower() for message in report.messages)
