"""Check relative Markdown links without requiring network access."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from collections.abc import Iterator
from urllib.parse import unquote


LINK_START = re.compile(r"!?\[[^]]*\]\(")


def link_targets(text: str) -> Iterator[str]:
    """Read inline destinations with balanced parentheses or angle brackets."""
    for match in LINK_START.finditer(text):
        start = match.end()
        depth = 1
        escaped = False
        for index in range(start, len(text)):
            char = text[index]
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    yield text[start:index]
                    break


def broken_links(root: str | Path) -> list[tuple[str, str]]:
    base = Path(root).resolve()
    broken: list[tuple[str, str]] = []
    for document in sorted(base.rglob("*.md")):
        for raw_target in link_targets(document.read_text(encoding="utf-8")):
            target = raw_target.strip()
            target = target[1:].split(">", 1)[0] if target.startswith("<") else target.split(" ", 1)[0]
            target = unquote(target.split("#", 1)[0])
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
