"""Render the starter kit's teaching and consulting infographics as SVG."""

from __future__ import annotations

import html
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "media" / "exports"
PAPER, INK, COBALT, CORAL, LIME, LAVENDER, MUTED = "#F7F5EF", "#0B1220", "#2C64F5", "#F27A5E", "#C8E86B", "#DCD7FE", "#5B657A"


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def text(x: float, y: float, value: str, *, size: int = 18, fill: str = INK, weight: int = 500, anchor: str = "start", family: str = "Arial,sans-serif") -> str:
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}px" font-weight="{weight}" text-anchor="{anchor}" fill="{fill}">{esc(value)}</text>'


def card(x: float, y: float, w: float, h: float, title: str, body: str, accent: str = COBALT) -> str:
    title_lines = textwrap.wrap(title, max(12, int((w - 60) / 12)))
    body_lines = [line for paragraph in body.split("\n") for line in (textwrap.wrap(paragraph, max(12, int((w - 60) / 8))) or [""])]
    parts = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="24" fill="#FFFFFF" stroke="{accent}" stroke-width="3"/><rect x="{x}" y="{y}" width="10" height="{h}" rx="5" fill="{accent}"/>']
    for index, line in enumerate(title_lines):
        parts.append(text(x + 30, y + 40 + index * 26, line, size=22, weight=700))
    start = y + 44 + len(title_lines) * 26
    for index, line in enumerate(body_lines):
        parts.append(text(x + 30, start + index * 22, line, size=16, fill=MUTED))
    return "".join(parts)


def node(cx: float, cy: float, label: str, color: str, radius: float = 62) -> str:
    parts = [f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{color}" stroke="{INK}" stroke-width="4"/>']
    lines = label.split("\n")
    for i, line in enumerate(lines):
        parts.append(text(cx, cy + (i - (len(lines) - 1) / 2) * 22 + 7, line, size=18, weight=700, anchor="middle", fill="#FFFFFF" if color == COBALT else INK))
    return "".join(parts)


def base(title: str, eyebrow: str, question: str, lesson: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 900" role="img" aria-labelledby="title desc"><title id="title">{esc(title)}</title><desc id="desc">{esc(lesson)}</desc>',
        f'<rect width="1400" height="900" fill="{PAPER}"/><circle cx="1270" cy="80" r="180" fill="{LAVENDER}" opacity=".48"/><path d="M0 770 C280 680 380 850 720 750 S1180 620 1400 710 V900 H0Z" fill="{INK}"/>',
        text(76, 72, eyebrow.upper(), size=16, fill=CORAL, weight=800, family="monospace"), text(76, 132, title, size=47, fill=INK, weight=800, family="Georgia,serif"), text(76, 182, question, size=21, fill=MUTED),
        text(76, 846, "ONTOLOGY STARTER KIT  /  EDITABLE SVG  /  EVIDENCE FIRST", size=13, fill="#B9C4D7", weight=700, family="monospace"),
    ]


def finish(parts: list[str], name: str) -> None:
    parts.append("</svg>")
    (OUT / name).write_text("".join(parts) + "\n", encoding="utf-8")


def one_word() -> None:
    p = base("One word. Three meanings.", "01 / shared language", "How do three teams make one definition safe to reuse?", "Three teams converge on a scoped Customer definition, with exclusions and a version that make the shared meaning testable.")
    p += [card(76, 260, 280, 170, "Sales", "A paying account", CORAL), card(76, 460, 280, 170, "Support", "The person who calls", COBALT), card(1044, 260, 280, 170, "Finance", "A legal entity", LIME), card(1044, 460, 280, 170, "Shared term", "Customer v1.2", LAVENDER)]
    p += [f'<path d="M356 345 C530 345 545 390 654 390" fill="none" stroke="{CORAL}" stroke-width="6" marker-end="url(#arrow)"/><path d="M356 545 C530 545 545 430 654 430" fill="none" stroke="{COBALT}" stroke-width="6" marker-end="url(#arrow)"/><path d="M1044 345 C880 345 855 390 746 390" fill="none" stroke="{LIME}" stroke-width="6" marker-end="url(#arrow)"/><path d="M1044 545 C880 545 855 430 746 430" fill="none" stroke="{LAVENDER}" stroke-width="6" marker-end="url(#arrow)"/>', node(700, 410, "Customer\nscoped", LIME, 92), card(500, 590, 400, 115, "Scope + exclusions", "Account, person, and lead stay distinct", COBALT), '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L8,4z" fill="#2C64F5"/></marker></defs>']
    finish(p, "infographic-one-word-three-meanings.svg")


def graph_layers() -> None:
    p = base("From glossary to graph", "02 / three layers", "What does an ontology add to a list of terms?", "The same Alpha service becomes progressively more useful as definitions, relations, and governed instances are added.")
    p += [card(76, 280, 340, 330, "Glossary", "Alpha service\n\nA named concept", CORAL), card(530, 280, 340, 330, "Ontology", "Service\nownedBy Team\nworksOn Project", COBALT), card(984, 280, 340, 330, "Knowledge graph", "ex:AlphaService\nex:Aurora\nex:ProjectAlpha", LIME), text(452, 445, "+ relations", size=18, fill=CORAL, weight=800, anchor="middle"), text(910, 445, "+ instances", size=18, fill=CORAL, weight=800, anchor="middle"), '<path d="M420 445 H510" stroke="#F27A5E" stroke-width="6" marker-end="url(#arrow)"/><path d="M874 445 H964" stroke="#F27A5E" stroke-width="6" marker-end="url(#arrow)"/>', '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L8,4z" fill="#F27A5E"/></marker></defs>']
    finish(p, "infographic-vocabulary-ontology-graph.svg")


def owl_shacl() -> None:
    p = base("Inference is not validation", "03 / semantics", "When should a graph infer, and when should it stop?", "A Manager is a Person. Given Maya is a Manager, RDFS/OWL semantics entail Maya is a Person. SHACL separately checks a required name.")
    p += [text(110, 285, "OWL / meaning", size=25, fill=COBALT, weight=800), text(790, 285, "SHACL / quality gate", size=25, fill=CORAL, weight=800), node(250, 440, "Manager", LIME), node(510, 440, "Person", LAVENDER), node(930, 410, "Maya\nPerson", LAVENDER), node(1190, 410, "name?", CORAL), '<path d="M315 440 H445" stroke="#2C64F5" stroke-width="6" marker-end="url(#arrow)"/><path d="M995 410 H1125" stroke="#F27A5E" stroke-width="6" marker-end="url(#arrow)"/>', text(380, 405, "subClassOf", size=16, fill=COBALT, weight=700, anchor="middle"), text(1060, 375, "minCount 1", size=16, fill=CORAL, weight=700, anchor="middle"), card(120, 610, 560, 110, "Derived", "Maya is a Manager → Maya is a Person", LIME), card(720, 610, 560, 110, "Rejected", "Missing name → fix before release", CORAL), '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L8,4z" fill="#2C64F5"/></marker></defs>']
    finish(p, "infographic-owl-versus-shacl.svg")


def question_evidence() -> None:
    p = base("A question becomes a trace", "04 / evidence", "Can a reader see why the answer is safe?", "A competency question moves through a named query, retrieved rows, assertion paths, and a versioned answer with explicit limitations.")
    stages = [(90, "Question", "Who manages Alpha?", CORAL), (350, "Named query", "manager.rq", COBALT), (610, "Rows", "Maya Chen", LAVENDER), (870, "Path", "Maya → manages → Aurora", LIME), (1130, "Answer", "Check support", COBALT)]
    for x, title, body, color in stages:
        p.append(card(x, 350, 220, 180, title, body, color))
    for x in (310, 570, 830, 1090):
        p.append(f'<path d="M{x} 440 H{x + 34}" stroke="{CORAL}" stroke-width="6" marker-end="url(#arrow)"/>')
    p += [card(370, 610, 660, 100, "Trace record", "data v0.2.0  ·  ex:Maya  ·  ex:Aurora  ·  source:crm-export-07", LIME), '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L8,4z" fill="#F27A5E"/></marker></defs>']
    finish(p, "infographic-question-to-evidence.svg")


def unknown_false() -> None:
    p = base("Unknown is a useful answer", "05 / open world", "What is the difference between absent and false?", "Under an open-world assumption, a missing triple is unknown; an explicit boolean false states a value for a specific property, subject to source review.")
    p += [text(120, 300, "No triple", size=26, fill=COBALT, weight=800), text(820, 300, "Explicit triple", size=26, fill=CORAL, weight=800), card(90, 350, 560, 190, "ex:ProjectAlpha  ex:active  ?", "No active value was retrieved", COBALT), card(750, 350, 560, 190, "ex:ProjectAlpha  ex:active  false", "An explicit boolean value for active", CORAL), node(365, 675, "UNKNOWN", LAVENDER, 92), node(1035, 675, "FALSE /\nACTIVE", CORAL, 92), text(365, 805, "Ask for evidence", size=18, fill="#B9C4D7", weight=700, anchor="middle"), text(1035, 805, "Act with provenance", size=18, fill="#B9C4D7", weight=700, anchor="middle")]
    finish(p, "infographic-unknown-versus-false.svg")


def reuse() -> None:
    p = base("Reuse before you mint", "06 / governance", "How do you avoid six competing Service classes?", "A reuse decision searches existing terms, checks scope and license, maps differences, and only then creates a new term.")
    points = [(190, 440, "SEARCH", COBALT), (460, 300, "DEFINE", CORAL), (460, 580, "SCOPE", LIME), (810, 300, "MAP", LAVENDER), (810, 580, "LICENSE", CORAL), (1160, 440, "REUSE", LIME)]
    for x, y, label, color in points:
        p.append(node(x, y, label, color, 70))
    for x1, y1, x2, y2 in [(255, 420, 395, 320), (255, 460, 395, 560), (525, 300, 740, 300), (525, 580, 740, 580), (880, 300, 1090, 420), (880, 580, 1090, 460)]:
        p.append(f'<path d="M{x1} {y1} Q{(x1+x2)/2} {(y1+y2)/2-45} {x2} {y2}" fill="none" stroke="{COBALT}" stroke-width="5" marker-end="url(#arrow)"/>')
    p += [text(700, 680, "If no safe match exists → mint with owner, version, and deprecation policy", size=18, fill=INK, weight=700, anchor="middle"), '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L8,4z" fill="#2C64F5"/></marker></defs>']
    finish(p, "infographic-reuse-before-mint.svg")


def life_science() -> None:
    p = base("An annotation needs a trail", "07 / life sciences", "Can another scientist reproduce the biological claim?", "A gene product annotation is useful only when the process, evidence code, reference, taxon, and review status travel with it.")
    p += [node(230, 440, "Annotation", COBALT, 85),
          node(710, 300, "Gene\nproduct", LAVENDER, 75),
          node(1070, 440, "GO process", LIME, 75),
          node(710, 600, "Evidence", CORAL, 75)]
    for end_x, end_y, label, label_x, label_y in [(630, 300, "annotates", 465, 320), (990, 440, "about process", 665, 410), (630, 600, "supported by", 465, 600)]:
        p.append(f'<path d="M315 440 Q460 {end_y} {end_x} {end_y}" fill="none" stroke="{COBALT}" stroke-width="5" marker-end="url(#arrow)"/>')
        p.append(text(label_x, label_y, label, size=18, fill=INK, weight=700, anchor="middle"))
    p += [text(80, 700, "SYNTHETIC EXAMPLE  /  evidence code + source span + taxon + review date", size=17, fill=INK), '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L8,4z" fill="#2C64F5"/></marker></defs>']
    finish(p, "infographic-life-science-evidence.svg")


def migration() -> None:
    p = base("Migrations need a landing zone", "08 / change", "What happens when a term is deprecated?", "A safe term migration names the replacement, publishes a mapping, tests old queries, and leaves a clear deprecation window.")
    p += [node(190, 435, "OldService", CORAL), node(500, 435, "mapping", LAVENDER), node(810, 435, "Service", LIME), node(1120, 435, "retest", COBALT), '<path d="M260 435 H430" stroke="#2C64F5" stroke-width="6" stroke-dasharray="10 8" marker-end="url(#arrow)"/><path d="M570 435 H740" stroke="#2C64F5" stroke-width="6" marker-end="url(#arrow)"/><path d="M880 435 H1050" stroke="#2C64F5" stroke-width="6" marker-end="url(#arrow)"/>', card(250, 620, 900, 105, "Deprecation record", "old: ex:OldService  →  new: ex:Service  ·  sunset: 2026-06-30", CORAL), '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L8,4z" fill="#2C64F5"/></marker></defs>']
    finish(p, "infographic-term-migration.svg")


def consulting() -> None:
    p = base("Consulting value chain", "consulting / decision map", "Where does a governed ontology pay back?", "A life-science consultancy can connect strategy, research, regulatory, manufacturing, and market decisions through shared concepts and evidence.")
    stages = [(100, "Strategy", "portfolio\nchoices", CORAL), (350, "Research", "targets +\nindications", COBALT), (600, "Regulatory", "claims +\nsubmission", LIME), (850, "Manufacture", "process +\nsite", LAVENDER), (1100, "Market", "access +\noutcomes", CORAL)]
    for x, title, body, color in stages:
        p.append(card(x, 350, 200, 190, title, body, color))
    for x in (300, 550, 800, 1050):
        p.append(f'<path d="M{x} 445 H{x + 44}" stroke="{COBALT}" stroke-width="6" marker-end="url(#arrow)"/>')
    p += [card(250, 625, 900, 105, "Consulting output", "A traceable recommendation: owner · evidence · confidence · next action", LIME), '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L8,4z" fill="#2C64F5"/></marker></defs>']
    finish(p, "consulting-value-chain.svg")


def evidence_room() -> None:
    p = base("The evidence room", "consulting / assurance", "How does a team separate supported, contested, and unknown?", "An evidence room gives consultants a review queue where each claim shows its sources, status, owner, and next action.")
    p += [card(90, 300, 360, 250, "Supported", "Claim 014\n2 independent sources\nreviewed by: R. Singh", LIME), card(520, 300, 360, 250, "Contested", "Claim 022\nsource dates disagree\nopen reviewer task", CORAL), card(950, 300, 360, 250, "Unknown", "Claim 031\nno source span\nabstain from answer", LAVENDER), text(270, 635, "publish", size=19, fill=MUTED, weight=800, anchor="middle"), text(700, 635, "investigate", size=19, fill=MUTED, weight=800, anchor="middle"), text(1130, 635, "request evidence", size=19, fill=MUTED, weight=800, anchor="middle")]
    finish(p, "consulting-evidence-room.svg")


def scorecard() -> None:
    p = base("Pilot scorecard", "consulting / illustrative targets", "Can the pilot show value without hiding uncertainty?", "A credible pilot pairs baseline and target metrics with evidence coverage and a boundary statement that prevents overclaiming.")
    p += [card(100, 300, 260, 210, "Cycle time", "baseline 14d\ntarget 8d", COBALT), card(410, 300, 260, 210, "Evidence", "coverage 62%\ntarget 90%", LIME), card(720, 300, 260, 210, "Rework", "baseline 18%\ntarget 10%", CORAL), card(1030, 300, 260, 210, "Adoption", "4 / 6 teams\ntarget 6 / 6", LAVENDER), card(250, 620, 900, 105, "Boundary", "Hypothetical figures for planning; replace them with measured pilot results.", CORAL)]
    finish(p, "consulting-pilot-scorecard.svg")


def claim_trace() -> None:
    p = base("Claim to source", "consulting / evidence chain", "Can a reviewer follow one assertion back to the exact source span?", "A claim is publishable only when its source record, exact span, graph path, and review decision remain connected.")
    stages = [(80, "Claim", "C-014\nasset target", CORAL), (360, "Source", "packet-v2", COBALT), (640, "Span", "p. 2, ¶3", LAVENDER), (920, "Graph path", "Asset → Claim\n→ Evidence", LIME), (1200, "Decision", "supported\nR. Singh", COBALT)]
    for x, title, body, color in stages:
        p.append(card(x, 360, 190, 180, title, body, color))
    for x in (270, 550, 830, 1110):
        p.append(f'<path d="M{x} 450 H{x + 72}" stroke="{CORAL}" stroke-width="6" marker-end="url(#arrow)"/>')
    p += [card(250, 635, 900, 100, "Fail closed", "Missing span, path, or reviewer → keep the claim in the queue", CORAL), '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L8,4z" fill="#F27A5E"/></marker></defs>']
    finish(p, "consulting-claim-to-source.svg")


def identity_crosswalk() -> None:
    p = base("Identity crosswalk", "consulting / reconciliation", "Which source records may share one canonical identity?", "Exact aliases can be approved; collisions and near matches stay visible in a review queue with reversible decisions.")
    p += [card(80, 290, 320, 180, "CRM-001", "Aurora Team\nexact alias", CORAL), card(80, 520, 320, 180, "LEGACY-003", "Aurora\ncollision", CORAL), card(540, 400, 320, 180, "Review queue", "approve · reject\nambiguous", LAVENDER), card(1000, 290, 320, 180, "Canonical", "TeamAurora\nversion v1", LIME), card(1000, 520, 320, 180, "Unresolved", "no sameAs\nno merge", COBALT), '<path d="M400 380 C465 380 475 430 530 440" fill="none" stroke="#2C64F5" stroke-width="6" marker-end="url(#arrow)"/><path d="M400 610 C465 610 475 520 530 500" fill="none" stroke="#F27A5E" stroke-width="6" marker-end="url(#arrow)"/><path d="M870 440 C930 430 940 380 990 380" fill="none" stroke="#2C64F5" stroke-width="6" marker-end="url(#arrow)"/><path d="M870 500 C930 520 940 610 990 610" fill="none" stroke="#F27A5E" stroke-width="6" marker-end="url(#arrow)"/>', '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L8,4z" fill="#2C64F5"/></marker></defs>']
    finish(p, "consulting-identity-crosswalk.svg")


def quality_impact() -> None:
    p = base("Change impact map", "consulting / quality + supply", "What must a quality owner review after one controlled change?", "A change control fans out through products, sites, suppliers, materials, processes, methods, and filings before a disposition is approved.")
    p += [node(180, 450, "Change\ncontrol", CORAL, 82), node(500, 300, "Product", LIME, 68), node(500, 600, "Supplier", COBALT, 68), node(820, 300, "Process +\nmethod", LAVENDER, 74), node(820, 600, "Site +\nmaterial", LAVENDER, 74), node(1140, 450, "Filing\nreview", CORAL, 76), '<path d="M255 430 Q370 300 430 300" fill="none" stroke="#2C64F5" stroke-width="5" marker-end="url(#arrow)"/><path d="M255 470 Q370 600 430 600" fill="none" stroke="#2C64F5" stroke-width="5" marker-end="url(#arrow)"/><path d="M570 300 H745" stroke="#2C64F5" stroke-width="5" marker-end="url(#arrow)"/><path d="M570 600 H745" stroke="#2C64F5" stroke-width="5" marker-end="url(#arrow)"/><path d="M895 300 Q1020 300 1070 430" fill="none" stroke="#2C64F5" stroke-width="5" marker-end="url(#arrow)"/><path d="M895 600 Q1020 600 1070 470" fill="none" stroke="#2C64F5" stroke-width="5" marker-end="url(#arrow)"/>', card(315, 735, 770, 80, "Suggested impact ≠ approved disposition", "Review owner records evidence, decision, and effective date", CORAL), '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="4" orient="auto"><path d="M0,0 L0,8 L8,4z" fill="#2C64F5"/></marker></defs>']
    finish(p, "consulting-quality-impact.svg")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for render in (one_word, graph_layers, owl_shacl, question_evidence, unknown_false, reuse, life_science, migration, consulting, evidence_room, scorecard, claim_trace, identity_crosswalk, quality_impact):
        render()


if __name__ == "__main__":
    main()
