"""Run the deterministic, review-before-insert extraction lesson."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from pyshacl import validate

from ontology_starterkit.extraction import extract_candidates, validate_candidates
from ontology_starterkit.packs import load_pack


EX = Namespace("https://ontology-starterkit.dev/life-science/")


def run(path: str | Path, *, model: str = "deterministic-rule-v1") -> dict[str, object]:
    fixture = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    candidates = extract_candidates(fixture["text"], fixture["allowed_terms"], source_id=fixture["source_id"], model=model)
    errors = validate_candidates(fixture["text"], candidates, set(fixture["allowed_terms"].values()))
    graph = Graph()
    product = URIRef(EX + "CandidateProduct")
    process = URIRef(EX + "CandidateProcess")
    evidence = URIRef(EX + "CandidateEvidence")
    annotation = URIRef(EX + "CandidateAnnotation")
    graph.add((product, RDF.type, EX.GeneProduct))
    graph.add((product, EX.name, Literal("Synthetic protein A")))
    graph.add((process, RDF.type, EX.BiologicalProcess))
    graph.add((process, EX.name, Literal("Synthetic stress response")))
    graph.add((process, EX.externalId, Literal("GO:0008150")))
    graph.add((evidence, RDF.type, EX.EvidenceRecord))
    graph.add((evidence, EX.reference, Literal("PMID:00000000 (synthetic reference)")))
    graph.add((evidence, EX.evidenceCode, Literal("ECO:0000269")))
    graph.add((evidence, EX.taxon, Literal("NCBITaxon:9606")))
    graph.add((evidence, EX.sourceVersion, Literal("GOA-synthetic-2025.01")))
    graph.add((evidence, EX.retrievedOn, Literal("2026-09-16")))
    graph.add((evidence, EX.reviewState, Literal("needs-review")))
    graph.add((annotation, RDF.type, EX.Annotation))
    graph.add((annotation, EX.annotates, product))
    graph.add((annotation, EX.aboutProcess, process))
    graph.add((annotation, EX.supportedBy, evidence))
    graph.add((annotation, EX.reviewState, Literal("needs-review")))
    pack = load_pack(Path(__file__).resolve().parents[1] / "examples/life-science-annotations")
    shapes = Graph().parse(pack.resolve(pack.manifest["shapes"]), format="turtle")
    conforms, _, report = validate(graph, shacl_graph=shapes)
    return {
        "source_id": fixture["source_id"],
        "model": model,
        "candidates": [candidate.as_dict() for candidate in candidates],
        "validation_errors": errors,
        "candidate_rdf_conforms": bool(conforms),
        "review_diff": {"insert": [str(triple) for triple in graph], "trusted_write_required": True},
        "shacl_report": str(report),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("fixture", type=Path)
    parser.add_argument("--model", default="deterministic-rule-v1")
    args = parser.parse_args()
    print(json.dumps(run(args.fixture, model=args.model), indent=2))


if __name__ == "__main__":
    main()
