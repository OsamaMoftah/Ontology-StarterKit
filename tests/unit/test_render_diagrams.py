from scripts.render_diagrams import render_model
import xml.etree.ElementTree as ET

import pytest


def test_render_model_writes_accessible_deterministic_svg(tmp_path):
    source = tmp_path / "model.mmd"
    source.write_text("flowchart LR\n  Person[Person] -->|manages| Team[Team]\n")
    target = tmp_path / "model.svg"
    render_model(source, target)
    text = target.read_text()
    assert '<title id="title">Ontology model</title>' in text
    assert '<desc id="desc">' in text
    assert "Person" in text and "manages" in text and "Team" in text
    assert text.startswith("<svg")


def test_render_model_supports_dotted_instances_and_layered_branches(tmp_path):
    source = tmp_path / "model.mmd"
    source.write_text(
        "flowchart LR\n"
        "  Person[Person] -->|manages| Team[Team]\n"
        "  Team -->|worksOn| Project[Project]\n"
        "  Person -. instance .-> Maya[Maya Chen]\n"
    )
    target = tmp_path / "model.svg"
    render_model(source, target)
    root = ET.fromstring(target.read_text())
    paths = list(root.iter("{http://www.w3.org/2000/svg}path"))
    assert any(path.attrib.get("data-kind") == "dotted" for path in paths)
    assert any(path.attrib.get("data-relation") == "worksOn" for path in paths)
    assert "Maya Chen" in target.read_text()


def test_render_model_fails_loudly_for_unsupported_edges(tmp_path):
    source = tmp_path / "model.mmd"
    source.write_text("flowchart LR\n  Person ==> Team\n")
    with pytest.raises(ValueError, match="unsupported Mermaid edge"):
        render_model(source, tmp_path / "model.svg")
