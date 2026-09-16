"""Render a sourced four-lane ontology history timeline."""

from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "media" / "exports" / "ontology-history-timeline.svg"
LANES = [("Business", "#F27A5E"), ("Life sciences", "#C8E86B"), ("Standards", "#2C64F5"), ("AI", "#DCD7FE")]
EVENTS = [
    ("1960", "MeSH", 1), ("1993", "Gruber", 0), ("1998", "GO begins", 1),
    ("2000", "RDF / OWL", 2), ("2007", "OBO Foundry", 1), ("2011", "Schema.org", 0),
    ("2013", "PROV-O", 2), ("2023", "PrimeKG", 1), ("2024", "GraphRAG", 3),
]


def render() -> None:
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 760" role="img" aria-labelledby="title desc"><title id="title">Ontology history across four lanes</title><desc id="desc">Sourced teaching timeline separating business, life science, standards, and AI milestones.</desc><rect width="1500" height="760" fill="#F7F5EF"/>']
    parts.append('<text x="70" y="70" font-family="Georgia,serif" font-size="44" font-weight="800" fill="#0B1220">Ontology history, four lanes</text>')
    parts.append('<text x="70" y="108" font-family="Arial,sans-serif" font-size="18" fill="#5B657A">Milestones are context; each claim has a source in docs/history.</text>')
    x0, x1 = 180, 1410
    for index, (label, color) in enumerate(LANES):
        y = 190 + index * 120
        parts.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="#B9C4D7" stroke-width="4"/><rect x="70" y="{y - 20}" width="90" height="40" rx="20" fill="{color}"/><text x="115" y="{y + 6}" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" font-weight="700" fill="#0B1220">{html.escape(label)}</text>')
    for index, (year, label, lane) in enumerate(EVENTS):
        x = x0 + 60 + index * 145
        y = 190 + lane * 120
        color = LANES[lane][1]
        parts.append(f'<circle cx="{x}" cy="{y}" r="12" fill="{color}" stroke="#0B1220" stroke-width="3"/><text x="{x}" y="{y - 27}" text-anchor="middle" font-family="monospace" font-size="14" font-weight="700" fill="#0B1220">{year}</text><text x="{x}" y="{y + 36}" text-anchor="middle" font-family="Arial,sans-serif" font-size="14" fill="#24324A">{html.escape(label)}</text>')
    parts.append('<text x="70" y="700" font-family="monospace" font-size="13" fill="#5B657A">SOURCES: Gruber · Gene Ontology · W3C RDF/OWL/PROV-O · OBO Foundry · Schema.org · PrimeKG · Microsoft GraphRAG</text></svg>')
    OUT.write_text("".join(parts) + "\n", encoding="utf-8")


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    render()
