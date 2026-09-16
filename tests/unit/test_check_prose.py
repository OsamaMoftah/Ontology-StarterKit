from scripts.check_prose import scan_text


def test_scan_text_reports_high_signal_phrase():
    findings = scan_text("README.md", "This is a practical starter repo.")
    assert findings[0].term == "practical"


def test_clear_instruction_has_no_findings():
    assert scan_text("README.md", "Run ontokit validate examples/hello-ontology.") == []
