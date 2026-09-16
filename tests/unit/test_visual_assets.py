from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[2]


def test_infographic_suite_is_accessible_and_complete():
    outputs = sorted((ROOT / "media/exports").glob("infographic-*.svg"))
    assert len(outputs) == 8
    for output in outputs:
        root = ET.fromstring(output.read_text())
        assert root.attrib["role"] == "img"
        assert root.attrib["aria-labelledby"] == "title desc"
        assert root.find("{http://www.w3.org/2000/svg}title").attrib["id"] == "title"
        assert root.find("{http://www.w3.org/2000/svg}desc").attrib["id"] == "desc"


def test_consulting_visuals_have_distinct_deliverables():
    names = {path.name for path in (ROOT / "media/exports").glob("consulting-*.svg") if path.name != "consulting-model.svg"}
    assert names == {
        "consulting-value-chain.svg", "consulting-evidence-room.svg", "consulting-pilot-scorecard.svg",
        "consulting-claim-to-source.svg", "consulting-identity-crosswalk.svg", "consulting-quality-impact.svg",
    }
