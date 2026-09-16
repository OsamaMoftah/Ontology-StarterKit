"""Find a small set of high-signal AI-writing patterns in public docs.

This is a style guard, not a grammar checker. The default mode prints findings
and exits successfully so contributors can review context. CI uses ``--strict``
against the small set of landing and decision documents where these phrases
hide marketing claims most often.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


TARGETS = (
    Path("README.md"),
    Path("docs/README.md"),
    Path("CONTRIBUTING.md"),
    Path("CODE_OF_CONDUCT.md"),
    Path("docs/for-product-managers/decision-framework.md"),
    Path("docs/for-product-managers/investment-one-pager.md"),
    Path("docs/for-product-managers/roi-calculator/README.md"),
    Path("docs/for-startups/30-day-sprint.md"),
    Path("docs/governance/release-process.md"),
    Path("src/integrations/langchain/kg-rag/README.md"),
    Path("src/integrations/langchain/kg-rag/graph_rag.py"),
)

PATTERNS = {
    "practical": re.compile(r"\bpractical\b", re.IGNORECASE),
    "intentionally": re.compile(r"\bintentionally\b", re.IGNORECASE),
    "first-class": re.compile(r"\bfirst[- ]class\b", re.IGNORECASE),
    "defensible": re.compile(r"\bdefensible\b", re.IGNORECASE),
    "engineering-backed": re.compile(r"\bengineering[- ]backed\b", re.IGNORECASE),
    "documentation-first": re.compile(r"\bdocumentation[- ]first\b", re.IGNORECASE),
    "validation-ready": re.compile(r"\bvalidation[- ]ready\b", re.IGNORECASE),
    "deliberately": re.compile(r"\bdeliberately\b", re.IGNORECASE),
    "tractable": re.compile(r"\btractable\b", re.IGNORECASE),
    "real AI products": re.compile(r"\breal AI products\b", re.IGNORECASE),
    "executive-ready": re.compile(r"\bexecutive[- ]ready\b", re.IGNORECASE),
}


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    term: str
    text: str


def scan_text(path: str | Path, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        for term, pattern in PATTERNS.items():
            if pattern.search(line):
                findings.append(Finding(str(path), line_number, term, line.strip()))
    return findings


def scan_repo(root: str | Path) -> list[Finding]:
    base = Path(root)
    findings: list[Finding] = []
    for relative in TARGETS:
        path = base / relative
        if path.exists():
            findings.extend(scan_text(relative, path.read_text(encoding="utf-8")))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="return nonzero when a target document contains a flagged phrase")
    args = parser.parse_args()
    findings = scan_repo(Path(__file__).resolve().parents[1])
    for finding in findings:
        print(f"{finding.path}:{finding.line}: {finding.term}: {finding.text}")
    return 1 if findings and args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
