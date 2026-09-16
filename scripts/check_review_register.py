"""Validate review registers and ensure every historical claim has a source link."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import yaml


REQUIRED_REVIEW_IDS = {"U10", "U13", "U24", "U25", "U26"}
REVIEW_STATUSES = {"awaiting-external-review", "approved", "approved-with-changes", "rejected"}


def check(root: str | Path = ".") -> dict[str, int]:
    root = Path(root).resolve()
    register = yaml.safe_load((root / "docs/reviews/domain-review-register.yaml").read_text(encoding="utf-8"))
    entries = register.get("entries", [])
    ids = {str(entry.get("id")) for entry in entries}
    if ids != REQUIRED_REVIEW_IDS:
        raise AssertionError(f"review register IDs differ: {sorted(ids)}")
    for entry in entries:
        if entry.get("status") not in REVIEW_STATUSES or not entry.get("reviewer_role") or not entry.get("review_questions"):
            raise AssertionError(f"incomplete review entry: {entry.get('id')}")
        for path in entry.get("internal_checks", []):
            if not (root / path).is_file():
                raise AssertionError(f"missing internal review artifact: {path}")
    source_register = yaml.safe_load((root / "docs/history/source-register.yaml").read_text(encoding="utf-8"))
    claims = source_register.get("claims", [])
    for claim in claims:
        document = root / claim["document"]
        text = document.read_text(encoding="utf-8")
        if claim["source"] not in text or not re.search(r"https?://", claim["source"]):
            raise AssertionError(f"historical source is not mapped in {document}: {claim['id']}")
    return {"review_entries": len(entries), "historical_claims": len(claims)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()
    print(check(args.root))


if __name__ == "__main__":
    main()
