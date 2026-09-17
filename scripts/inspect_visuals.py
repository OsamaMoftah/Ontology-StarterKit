"""Render SVG assets at their target viewports and check canvas dimensions."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SVG_NS = "{http://www.w3.org/2000/svg}"


def png_size(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"renderer did not produce PNG: {path}")
    return struct.unpack(">II", data[16:24])


def inspect(root: str | Path = ROOT, output_dir: str | Path | None = None) -> dict[str, object]:
    root = Path(root).resolve()
    renderer = shutil.which("playwright")
    if renderer is None:
        raise RuntimeError("playwright CLI is required for pixel-level SVG inspection")
    exports = root / "media/exports"
    assets = [(path, (1400, 900)) for path in sorted(exports.glob("infographic-*.svg"))]
    assets += [(path, (1400, 900)) for path in sorted(exports.glob("consulting-*.svg")) if path.stem != "consulting-model"]
    assets += [(exports / "consulting-model.svg", (1150, 385))]
    assets += [(path, (390, 844)) for path in sorted(exports.glob("mobile-*.svg"))]
    if len(assets) != 29:
        raise AssertionError(f"expected 29 teaching and consulting SVGs, found {len(assets)}")
    with tempfile.TemporaryDirectory(prefix="ontokit-visual-inspection-") as temporary:
        destination = Path(output_dir).resolve() if output_dir else Path(temporary)
        destination.mkdir(parents=True, exist_ok=True)
        checked: list[dict[str, object]] = []
        for path, expected_size in assets:
            tree = ET.parse(path)
            svg = tree.getroot()
            view_box = tuple(float(value) for value in (svg.get("viewBox") or "").split())
            if len(view_box) != 4 or (int(view_box[2]), int(view_box[3])) != expected_size:
                raise AssertionError(f"{path.name} has viewBox {view_box}, expected {expected_size}")
            rendered = destination / f"{path.stem}.png"
            subprocess.run(
                [renderer, "screenshot", f"--viewport-size={expected_size[0]},{expected_size[1]}", f"file://{path}", str(rendered)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            actual_size = png_size(rendered)
            if actual_size != expected_size:
                raise AssertionError(f"{path.name} rendered at {actual_size}, expected {expected_size}")
            checked.append({"asset": str(path.relative_to(root)), "viewport": expected_size, "render": str(rendered)})
        return {"assets": len(checked), "desktop_and_mobile_dimensions": True, "checked": checked}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    result = inspect(args.root, args.output_dir)
    print({"assets": result["assets"], "desktop_and_mobile_dimensions": result["desktop_and_mobile_dimensions"]})


if __name__ == "__main__":
    main()
