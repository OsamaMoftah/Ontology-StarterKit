"""Render Mermaid pack models to dependency-free, accessible SVG."""

from __future__ import annotations

import argparse
import html
import re
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Edge:
    left: str
    right: str
    relation: str
    kind: str = "solid"


NODE = re.compile(r"(?P<id>[A-Za-z][A-Za-z0-9_]*)(?:\[(?P<label>[^]]+)\])?")
SOLID = re.compile(r"(?P<left>[A-Za-z][A-Za-z0-9_]*)(?:\[(?P<ll>[^]]+)\])?\s+-->(?:\|(?P<label>[^|]+)\|)?\s+(?P<right>[A-Za-z][A-Za-z0-9_]*)(?:\[(?P<rl>[^]]+)\])?")
DOTTED = re.compile(r"(?P<left>[A-Za-z][A-Za-z0-9_]*)(?:\[(?P<ll>[^]]+)\])?\s+-\.\s*(?P<label>[^.]+?)\s*\.->\s+(?P<right>[A-Za-z][A-Za-z0-9_]*)(?:\[(?P<rl>[^]]+)\])?")
UNSUPPORTED = re.compile(r"(?P<left>[A-Za-z][A-Za-z0-9_]*).*?(?:==>|--x|---|-.+->).*?(?P<right>[A-Za-z][A-Za-z0-9_]*)")


def _parse(source: str) -> tuple[list[Edge], dict[str, str]]:
    edges: list[Edge] = []
    labels: dict[str, str] = {}
    for line_number, raw_line in enumerate(source.splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("%%") or line.startswith("flowchart") or line.startswith("graph"):
            continue
        dotted = DOTTED.fullmatch(line)
        solid = SOLID.fullmatch(line)
        match = dotted or solid
        if match:
            kind = "dotted" if dotted else "solid"
            edges.append(Edge(match.group("left"), match.group("right"), (match.group("label") or "related to").strip(), kind))
            for key, value in ((match.group("left"), match.group("ll")), (match.group("right"), match.group("rl"))):
                if value:
                    labels[key] = value.strip()
            continue
        if "-->" in line or ".->" in line or UNSUPPORTED.search(line):
            raise ValueError(f"unsupported Mermaid edge on line {line_number}: {line}")
        declaration = NODE.fullmatch(line)
        if declaration is None:
            raise ValueError(f"unsupported Mermaid syntax on line {line_number}: {line}")
        labels.setdefault(declaration.group("id"), declaration.group("label") or declaration.group("id"))
    if not edges:
        raise ValueError("no supported Mermaid relationships found")
    return edges, labels


def _layout(edges: list[Edge], nodes: list[str]) -> dict[str, tuple[int, int]]:
    outgoing: dict[str, set[str]] = defaultdict(set)
    indegree = {node: 0 for node in nodes}
    for edge in edges:
        if edge.right not in outgoing[edge.left]:
            outgoing[edge.left].add(edge.right)
            indegree[edge.right] += 1
    queue: deque[str] = deque(node for node in nodes if indegree[node] == 0)
    level = {node: 0 for node in nodes}
    visited: set[str] = set()
    while queue:
        node = queue.popleft()
        visited.add(node)
        for child in outgoing[node]:
            level[child] = max(level[child], level[node] + 1)
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if len(visited) != len(nodes):
        raise ValueError("cyclic models require a full Mermaid renderer")
    columns: dict[int, list[str]] = defaultdict(list)
    for node in nodes:
        columns[level[node]].append(node)
    positions: dict[str, tuple[int, int]] = {}
    for column, column_nodes in sorted(columns.items()):
        for row, node in enumerate(column_nodes):
            positions[node] = (190 + column * 250, 125 + row * 150)
    return positions


def _wrap(label: str, limit: int = 18) -> list[str]:
    words = label.split()
    lines: list[str] = []
    current = ""
    for word in words:
        if current and len(current) + len(word) + 1 > limit:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    if current:
        lines.append(current)
    return lines or [""]


def render_model(source: str | Path, target: str | Path) -> None:
    """Render a constrained Mermaid flowchart with truthful topology."""
    text = Path(source).read_text(encoding="utf-8")
    edges, labels = _parse(text)
    nodes = list(dict.fromkeys([node for edge in edges for node in (edge.left, edge.right)]))
    positions = _layout(edges, nodes)
    max_x = max(x for x, _ in positions.values())
    max_y = max(y for _, y in positions.values())
    width, height = max(760, max_x + 210), max(320, max_y + 110)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Ontology model</title>',
        '<desc id="desc">Nodes and labeled relationships from the reviewed Mermaid model.</desc>',
        '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#2C64F5"/></marker></defs>',
    ]
    for index, edge in enumerate(edges):
        x1, y1 = positions[edge.left]
        x2, y2 = positions[edge.right]
        start_x, end_x = x1 + 84, x2 - 84
        path = f"M {start_x} {y1} C {start_x + 70} {y1}, {end_x - 70} {y2}, {end_x} {y2}"
        dash = ' stroke-dasharray="7 6"' if edge.kind == "dotted" else ""
        parts.append(f'<path d="{path}" fill="none" stroke="#2C64F5" stroke-width="3"{dash} marker-end="url(#arrow)" data-edge="{index}" data-source="{html.escape(edge.left)}" data-relation="{html.escape(edge.relation)}" data-target="{html.escape(edge.right)}" data-kind="{edge.kind}"/>')
        label_x, label_y = (start_x + end_x) / 2, (y1 + y2) / 2 - 18
        label = html.escape(edge.relation)
        label_width = max(68, len(edge.relation) * 9)
        parts.append(f'<rect x="{label_x - label_width / 2:.1f}" y="{label_y - 17:.1f}" width="{label_width}" height="24" rx="12" fill="#F7F5EF" stroke="#DCD7FE"/>')
        parts.append(f'<text x="{label_x:.1f}" y="{label_y:.1f}" text-anchor="middle" font-family="Arial,sans-serif" font-size="13" fill="#24324A">{label}</text>')
    for node, (x, y) in positions.items():
        display = labels.get(node, node)
        lines = _wrap(display)
        box_height = max(70, 28 + len(lines) * 20)
        parts.append(f'<rect x="{x - 84}" y="{y - box_height / 2:.1f}" width="168" height="{box_height}" rx="18" fill="#EEF3FF" stroke="#2C64F5" stroke-width="2"/>')
        for row, line in enumerate(lines):
            baseline = y + (row - (len(lines) - 1) / 2) * 20 + 5
            parts.append(f'<text x="{x}" y="{baseline:.1f}" text-anchor="middle" font-family="Arial,sans-serif" font-size="15" font-weight="600" fill="#0B1220">{html.escape(line)}</text>')
    parts.append("</svg>")
    Path(target).write_text("".join(parts) + "\n", encoding="utf-8")


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
    outputs = {"hello-ontology": "hello-model.svg", "business-projects": "business-model.svg", "life-science-annotations": "life-science-model.svg", "consulting-evidence-room": "consulting-model.svg"}
    for pack_id, output in outputs.items():
        render_model(root / "examples" / pack_id / "model.mmd", root / "media" / "exports" / output)


if __name__ == "__main__":
    main()
