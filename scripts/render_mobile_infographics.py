"""Generate dedicated 390px portrait compositions for the teaching graphics."""

from __future__ import annotations

import html
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "media" / "exports"
PAPER, INK, BLUE, CORAL, LIME = "#F7F5EF", "#0B1220", "#2C64F5", "#F27A5E", "#C8E86B"

CARDS = {
    "one-word-three-meanings": ("One word. Three meanings.", "Sales, support, and finance scope Customer differently.", ["Sales: paying account", "Support: caller", "Finance: legal entity", "Decision: define exclusions"]),
    "vocabulary-ontology-graph": ("Glossary to graph", "A graph adds relationships and governed instances.", ["Glossary: Service", "Ontology: ownedBy Team", "Graph: ex:AlphaService", "Check: query an instance"]),
    "owl-versus-shacl": ("Inference is not validation", "Manager is a subclass of Person; SHACL checks required data.", ["Manager → Person", "Maya is a Manager", "Maya is therefore a Person", "Missing name: reject"]),
    "question-to-evidence": ("A question becomes a trace", "A named query turns a question into inspectable evidence.", ["Question: who manages Alpha?", "Query: manager.rq", "Row: Maya Chen", "Path: Maya → manages → Aurora"]),
    "unknown-versus-false": ("Unknown is useful", "An absent value is not a false value.", ["No active assertion: unknown", "active false: explicit value", "Keep the property and source visible", "Abstain when evidence is missing"]),
    "reuse-before-mint": ("Reuse before you mint", "Search, scope, map, and check license before adding a term.", ["Search existing terms", "Define scope", "Map differences", "Reuse or mint with an owner"]),
    "life-science-evidence": ("An annotation needs a trail", "The annotation carries context for review.", ["Annotation → gene product", "Annotation → biological process", "Annotation → evidence record", "Keep code, reference, taxon, and date"]),
    "term-migration": ("Migrations need a landing zone", "A deprecated term needs a tested replacement.", ["OldService", "Mapping", "Service", "Retest old questions"]),
    "consulting-value-chain": ("Consulting value chain", "Connect strategy, research, regulatory, manufacturing, and market decisions.", ["Strategy", "Research", "Regulatory", "Manufacture", "Market"]),
    "consulting-evidence-room": ("The evidence room", "Separate supported, contested, and unknown claims.", ["Supported: publish", "Contested: investigate", "Unknown: request evidence"]),
    "consulting-pilot-scorecard": ("Pilot scorecard", "Pair a baseline and target with a boundary.", ["Cycle time: baseline → target", "Evidence coverage", "Rework", "Boundary: hypothetical until measured"]),
    "consulting-claim-to-source": ("Claim to source", "Follow one assertion to its exact evidence span and review decision.", ["Claim: C-014", "Source: packet-v2", "Span: p. 2, paragraph 3", "Path + reviewer decision"]),
    "consulting-identity-crosswalk": ("Identity crosswalk", "Approve exact aliases and keep collisions unresolved.", ["Source IDs stay intact", "Review queue: approve or reject", "Canonical mapping version", "Collision: no merge"]),
    "consulting-quality-impact": ("Change impact map", "Trace a controlled change before approving disposition.", ["Change control", "Product, site, supplier, material", "Process, method, filing", "Suggested impact needs review"]),
}


def render(name: str, title: str, lesson: str, items: list[str]) -> None:
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 390 844" role="img" aria-labelledby="title desc"><title id="title">{html.escape(title)}</title><desc id="desc">{html.escape(lesson)}</desc><rect width="390" height="844" fill="{PAPER}"/>']
    parts.append(f'<text x="24" y="48" font-family="Arial,sans-serif" font-size="12" font-weight="800" fill="{CORAL}">ONTOLOGY STARTER KIT</text>')
    y = 92
    for line in textwrap.wrap(title, 22):
        parts.append(f'<text x="24" y="{y}" font-family="Georgia,serif" font-size="30" font-weight="800" fill="{INK}">{html.escape(line)}</text>')
        y += 36
    y += 14
    for line in textwrap.wrap(lesson, 42):
        parts.append(f'<text x="24" y="{y}" font-family="Arial,sans-serif" font-size="15" fill="#5B657A">{html.escape(line)}</text>')
        y += 22
    y += 24
    for index, item in enumerate(items):
        color = [BLUE, CORAL, LIME][index % 3]
        lines = textwrap.wrap(item, 31)
        height = max(72, 32 + 21 * len(lines))
        parts.append(f'<rect x="24" y="{y}" width="342" height="{height}" rx="16" fill="#FFFFFF" stroke="{color}" stroke-width="3"/>')
        parts.append(f'<circle cx="52" cy="{y + 27}" r="10" fill="{color}"/>')
        for row, line in enumerate(lines):
            parts.append(f'<text x="76" y="{y + 34 + row * 21}" font-family="Arial,sans-serif" font-size="16" fill="{INK}">{html.escape(line)}</text>')
        y += height + 14
    parts.append(f'<path d="M0 790 Q100 750 200 790 T390 770 V844 H0Z" fill="{INK}"/><text x="24" y="820" font-family="monospace" font-size="10" fill="#B9C4D7">READ THE TEXT EQUIVALENT FOR DETAILS</text></svg>')
    (OUT / f"mobile-{name}.svg").write_text("".join(parts) + "\n", encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (title, lesson, items) in CARDS.items():
        render(name, title, lesson, items)


if __name__ == "__main__":
    main()
