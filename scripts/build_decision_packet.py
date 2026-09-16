"""Build a reproducible evidence-room decision packet from a reviewed pack."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ontology_starterkit.evals import evaluate_query
from ontology_starterkit.packs import load_pack
from ontology_starterkit.validation import run_named_query, validate_pack


def build_packet(pack_path: str | Path) -> dict[str, object]:
    pack = load_pack(pack_path)
    validation = validate_pack(pack)
    queries: dict[str, object] = {}
    for query_id in pack.manifest["queries"]:
        queries[query_id] = {"rows": run_named_query(pack, query_id), "evaluation": evaluate_query(pack, query_id)}
    return {
        "pack": pack.pack_id,
        "version": pack.manifest["version"],
        "validation": {"conforms": validation.conforms, "messages": list(validation.messages)},
        "queries": queries,
        "provenance": {"sources_file": pack.manifest["sources"], "license": pack.manifest["license"]},
        "limitations": ["Synthetic teaching data; not clinical, regulatory, or investment advice.", "Query output does not establish source entailment."],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pack", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(build_packet(args.pack), indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
