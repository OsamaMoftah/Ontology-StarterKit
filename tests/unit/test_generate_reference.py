from scripts.generate_reference import generate_reference


def test_reference_contains_classes_and_properties():
    reference = generate_reference("examples/business-projects/ontology.ttl")
    assert "## Classes" in reference
    assert "https://ontology-starterkit.dev/business/Team" in reference
    assert "https://ontology-starterkit.dev/business/owns" in reference
