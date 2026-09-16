from scripts.render_diagrams import render_model


def test_render_model_writes_accessible_deterministic_svg(tmp_path):
    source = tmp_path / "model.mmd"
    source.write_text("flowchart LR\n  Person[Person] -->|manages| Team[Team]\n")
    target = tmp_path / "model.svg"
    render_model(source, target)
    text = target.read_text()
    assert '<title>Ontology model</title>' in text
    assert "Person" in text and "manages" in text and "Team" in text
    assert text.startswith("<svg")
