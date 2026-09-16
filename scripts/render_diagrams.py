"""Render the small pack diagrams to dependency-free, accessible SVG."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


EDGE = re.compile(r"(?P<left>[A-Za-z0-9_]+)(?:\[[^]]+\])?\s+-->(?:\|(?P<label>[^|]+)\|)?\s+(?P<right>[A-Za-z0-9_]+)(?:\[[^]]+\])?")


def render_model(source: str | Path, target: str | Path) -> None:
    """Render a simple Mermaid flowchart as an inspectable SVG."""
    text = Path(source).read_text()
    edges = EDGE.findall(text)
    nodes: list[str] = []
    for left, label, right in edges:
        for node in (left, right):
            if node not in nodes:
                nodes.append(node)
    width = max(420, len(nodes) * 180)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} 180" role="img" aria-labelledby="title desc">', '<title>Ontology model</title>', '<desc>Nodes and labeled relationships from the reviewed Mermaid model.</desc>']
    positions = {node: 90 + index * 180 for index, node in enumerate(nodes)}
    for left, label, right in edges:
        x1, x2 = positions[left], positions[right]
        parts.append(f'<line x1="{x1 + 60}" y1="80" x2="{x2 - 60}" y2="80" stroke="#5271ff" stroke-width="2" marker-end="url(#arrow)"/>')
        if label:
            parts.append(f'<text x="{(x1 + x2) / 2}" y="65" text-anchor="middle" font-family="sans-serif" font-size="13">{html.escape(label)}</text>')
    for node, x in positions.items():
        parts.append(f'<rect x="{x - 60}" y="50" width="120" height="60" rx="10" fill="#eef2ff" stroke="#3f51b5"/>')
        parts.append(f'<text x="{x}" y="85" text-anchor="middle" font-family="sans-serif" font-size="15">{html.escape(node)}</text>')
    parts.append('<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#5271ff"/></marker></defs></svg>')
    Path(target).write_text("".join(parts) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, nargs="?")
    parser.add_argument("target", type=Path, nargs="?")
    args = parser.parse_args()
    if (args.source is None) != (args.target is None):
        parser.error("source and target must be provided together")
    if args.source is not None and args.target is not None:
        render_model(args.source, args.target)
        return
    root = Path(__file__).resolve().parents[1]
    outputs = {
        "hello-ontology": "hello-model.svg",
        "business-projects": "business-model.svg",
        "life-science-annotations": "life-science-model.svg",
    }
    for pack_id, output in outputs.items():
        render_model(root / "examples" / pack_id / "model.mmd", root / "media" / "exports" / output)


if __name__ == "__main__":
    main()
