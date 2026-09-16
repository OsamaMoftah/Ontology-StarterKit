from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]


def test_mobile_visual_suite_has_portrait_compositions():
    outputs = sorted((ROOT / "media/exports").glob("mobile-*.svg"))
    assert len(outputs) == 14
    for output in outputs:
        root = ET.fromstring(output.read_text())
        assert root.attrib["viewBox"] == "0 0 390 844"
        assert root.attrib["role"] == "img"
