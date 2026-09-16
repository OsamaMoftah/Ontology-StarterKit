"""Check relative Markdown links without requiring network access."""

from __future__ import annotations

import re
import sys
from pathlib import Path


LINK = re.compile(r"!?(?:\[[^]]*\])\(([^)]+)\)")


def broken_links(root: str | Path) -> list[tuple[str, str]]:
    base = Path(root).resolve()
    broken: list[tuple[str, str]] = []
    for document in sorted(base.rglob("*.md")):
        for raw_target in LINK.findall(document.read_text(encoding="utf-8")):
            target = raw_target.strip().split("#", 1)[0].split(" ", 1)[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            candidate = (document.parent / target).resolve()
            try:
                candidate.relative_to(base)
            except ValueError:
                broken.append((str(document.relative_to(base)), raw_target))
                continue
            if not candidate.exists():
                broken.append((str(document.relative_to(base)), raw_target))
    return broken


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    failures = broken_links(root)
    for document, target in failures:
        print(f"{document}: missing relative link {target}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
