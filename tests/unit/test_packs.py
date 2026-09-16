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


def test_load_pack_rejects_path_escape(tmp_path):
    pack = tmp_path / "pack"
    pack.mkdir()
    (pack / "manifest.yaml").write_text("id: demo\nontology: ../outside.ttl\n")
    with pytest.raises(PackError, match="path"):
        load_pack(pack)
