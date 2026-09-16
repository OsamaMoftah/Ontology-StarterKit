from scripts.check_links import broken_links


def test_broken_links_reports_missing_relative_target(tmp_path):
    (tmp_path / "README.md").write_text("[missing](nope.md)\n")
    assert broken_links(tmp_path) == [("README.md", "nope.md")]


def test_broken_links_ignores_urls_and_existing_targets(tmp_path):
    (tmp_path / "README.md").write_text("[ok](docs.md) [web](https://example.com)\n")
    (tmp_path / "docs.md").write_text("ok")
    assert broken_links(tmp_path) == []
