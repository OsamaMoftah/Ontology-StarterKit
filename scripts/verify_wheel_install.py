"""Install a wheel into a clean environment outside the checkout and run a query."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def verify(wheel: str | Path, examples: str | Path) -> None:
    wheel = Path(wheel).resolve()
    examples = Path(examples).resolve()
    with tempfile.TemporaryDirectory(prefix="ontokit-wheel-") as directory:
        root = Path(directory)
        env = root / "venv"
        subprocess.run([sys.executable, "-m", "venv", str(env)], check=True)
        python = env / "bin" / "python"
        if not python.exists():
            python = env / "Scripts" / "python.exe"
        subprocess.run([str(python), "-m", "pip", "install", str(wheel)], check=True, stdout=subprocess.DEVNULL)
        copied = root / "examples"
        shutil.copytree(examples, copied)
        subprocess.run([
            str(python), "-c",
            "from ontology_starterkit.packs import load_pack; from ontology_starterkit.validation import run_named_query; print(run_named_query(load_pack('examples/hello-ontology'), 'manager'))",
        ], check=True, cwd=root)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("wheel", type=Path)
    parser.add_argument("--examples", type=Path, default=Path("examples"))
    args = parser.parse_args()
    verify(args.wheel, args.examples)


if __name__ == "__main__":
    main()
