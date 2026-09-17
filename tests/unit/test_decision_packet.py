from scripts.build_decision_packet import build_packet


def test_decision_packet_contains_results_provenance_and_limits():
    packet = build_packet("examples/consulting-evidence-room")
    assert packet["validation"]["conforms"] is True
    assert packet["queries"]["claim-status"]["evaluation"]["passed"] is True
    assert packet["provenance"]["license"] == "CC0-1.0 synthetic teaching data"
    assert packet["limitations"]
