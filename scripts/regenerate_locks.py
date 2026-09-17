"""Regenerate universal and supported-Python dependency locks."""

from __future__ import annotations

import argparse
from collections.abc import Callable
from pathlib import Path
import subprocess
import tempfile


TARGETS = {
    "core": (Path("requirements/core.in"), Path("requirements/core.universal.lock")),
    "optional": (Path("requirements/optional.in"), Path("requirements/optional.universal.lock")),
}
SUPPORTED_PYTHON_VERSIONS = ("3.10", "3.11", "3.12")
DEFAULT_PYTHON_PLATFORM = "x86_64-unknown-linux-gnu"


def versioned_targets() -> dict[str, tuple[Path, Path, str]]:
    return {
        f"{name}-py{version.replace('.', '')}": (source, Path(f"requirements/{name}-py{version.replace('.', '')}.lock"), version)
        for name, (source, _) in TARGETS.items()
        for version in SUPPORTED_PYTHON_VERSIONS
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


def render_versioned(
    root: Path, source: Path, destination: Path, version: str, python_platform: str, output: Path
) -> None:
    subprocess.run(
        [
            "uv", "pip", "compile", str(source), "--python-version", version,
            "--python-platform", python_platform,
            "--custom-compile-command", f"uv pip compile {source} --python-version {version} --python-platform {python_platform} --output-file {destination}",
            "--output-file", str(output),
        ],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )


def verify_one(root_path: Path, destination: Path, render_fn: Callable[..., None], *render_args: object) -> None:
    with tempfile.NamedTemporaryFile(prefix="lock-", suffix=".lock") as temporary:
        temporary_path = Path(temporary.name)
    try:
        render_fn(root_path, *render_args, temporary_path)
        expected = (root_path / destination).read_bytes()
        actual = temporary_path.read_bytes()
        if actual != expected:
            raise AssertionError(f"{destination} is stale; run python scripts/regenerate_locks.py --write")
    finally:
        temporary_path.unlink(missing_ok=True)


def verify(
    root: str | Path = ".", *, include_universal: bool = True, python_platform: str = DEFAULT_PYTHON_PLATFORM
) -> dict[str, object]:
    root_path = Path(root).resolve()
    checked: list[str] = []
    if include_universal:
        for name, (_, destination) in TARGETS.items():
            verify_one(root_path, destination, render, name)
            checked.append(str(destination))
    for name, (source, destination, version) in versioned_targets().items():
        verify_one(root_path, destination, render_versioned, source, destination, version, python_platform)
        checked.append(str(destination))
    return {
        "checked": checked,
        "universal": include_universal,
        "python_versions": list(SUPPORTED_PYTHON_VERSIONS),
        "python_platform": python_platform,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--versioned-only", action="store_true")
    parser.add_argument("--python-platform", default=DEFAULT_PYTHON_PLATFORM)
    args = parser.parse_args()
    root = args.root.resolve()
    if args.write:
        if not args.versioned_only:
            for name, (_, destination) in TARGETS.items():
                with tempfile.NamedTemporaryFile(prefix=f"{name}-lock-", suffix=".lock") as temporary:
                    temporary_path = Path(temporary.name)
                try:
                    render(root, name, temporary_path)
                    temporary_path.replace(root / destination)
                finally:
                    temporary_path.unlink(missing_ok=True)
        for name, (source, destination, version) in versioned_targets().items():
            with tempfile.NamedTemporaryFile(prefix=f"{name}-lock-", suffix=".lock") as temporary:
                temporary_path = Path(temporary.name)
            try:
                render_versioned(root, source, destination, version, args.python_platform, temporary_path)
                temporary_path.replace(root / destination)
            finally:
                temporary_path.unlink(missing_ok=True)
    print(verify(root, include_universal=not args.versioned_only, python_platform=args.python_platform))


if __name__ == "__main__":
    main()
