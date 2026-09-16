"""Generate a small Markdown ontology reference from canonical Turtle."""

from __future__ import annotations

import argparse
from pathlib import Path
from rdflib import Graph, RDF, RDFS, OWL


def generate_reference(ontology: str | Path) -> str:
    graph = Graph().parse(ontology, format="turtle")
    lines = [f"# Ontology reference: {Path(ontology).parent.name}", "", "Generated from the canonical Turtle file. Review definitions and constraints before publication.", "", "## Classes", ""]
    classes = sorted(graph.subjects(RDF.type, OWL.Class), key=str)
    for item in classes:
        label = next(iter(graph.objects(item, RDFS.label)), "")
        lines.append(f"- `{item}`" + (f" — {label}" if label else ""))
    lines.extend(["", "## Properties", ""])
    properties = sorted(set(graph.subjects(RDF.type, OWL.ObjectProperty)) | set(graph.subjects(RDF.type, OWL.DatatypeProperty)), key=str)
    for item in properties:
        domain = next(iter(graph.objects(item, RDFS.domain)), "")
        range_ = next(iter(graph.objects(item, RDFS.range)), "")
        lines.append(f"- `{item}`" + (f" — domain `{domain}`" if domain else "") + (f", range `{range_}`" if range_ else ""))
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ontology", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(generate_reference(args.ontology), encoding="utf-8")


if __name__ == "__main__":
    main()
