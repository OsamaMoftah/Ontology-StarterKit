# Consulting evidence room

This fictional pack shows how a consulting evidence brief can distinguish a supported claim from an unsupported, conflicting, or stale one. Each claim carries an explicit review state, reviewer, and review date; source records carry a version and retrieval dates. The data is synthetic; it is not a client case study, clinical evidence, investment recommendation or representation of McKinsey, PwC, Strategy&, or another firm.

Run `python scripts/build_decision_packet.py examples/consulting-evidence-room /tmp/evidence-room-packet.json` to produce a reproducible packet containing every named-query result, expected fixture, source metadata, and limitations. The packet records evidence-link status; a link alone is not a reviewed support decision.
