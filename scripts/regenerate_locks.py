"""Regenerate the universal dependency locks for all supported platforms."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import tempfile


TARGETS = {
    "core": (Path("requirements/core.in"), Path("requirements/core.universal.lock")),
    "optional": (Path("requirements/optional.in"), Path("requirements/optional.universal.lock")),
}


def render(root: Path, name: str, output: Path) -> None:
    source, _ = TARGETS[name]
    destination = TARGETS[name][1]
    subprocess.run(
        [
            "uv", "pip", "compile", str(source), "--universal",
            "--custom-compile-command", f"uv pip compile {source} --universal --output-file {destination}",
            "--output-file", str(output),
        ],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )


def verify(root: str | Path = ".") -> dict[str, object]:
    root_path = Path(root).resolve()
    checked: list[str] = []
    for name, (_, destination) in TARGETS.items():
        with tempfile.NamedTemporaryFile(prefix=f"{name}-lock-", suffix=".lock") as temporary:
            temporary_path = Path(temporary.name)
        try:
            render(root_path, name, temporary_path)
            expected = (root_path / destination).read_bytes()
            actual = temporary_path.read_bytes()
            if actual != expected:
                raise AssertionError(f"{destination} is stale; run python scripts/regenerate_locks.py")
            checked.append(str(destination))
        finally:
            temporary_path.unlink(missing_ok=True)
    return {"checked": checked, "universal": True}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    if args.write:
        for name, (_, destination) in TARGETS.items():
            render(root, name, root / destination)
    print(verify(root))


if __name__ == "__main__":
    main()
