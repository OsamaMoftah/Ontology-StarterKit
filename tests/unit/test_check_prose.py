from scripts.check_prose import scan_text, scan_repo


def test_scan_text_reports_high_signal_phrase():
    findings = scan_text("README.md", "This is a practical starter repo.")
    assert findings[0].term == "practical"


def test_current_public_docs_pass_the_prose_guard():
    assert scan_repo(".") == []
