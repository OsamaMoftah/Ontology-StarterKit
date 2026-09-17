"""Run the positive commands used by the beginner and consulting lessons."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def verify(repo: str | Path = ".") -> list[dict[str, object]]:
    root = Path(repo).resolve()
    python = sys.executable
    with tempfile.TemporaryDirectory(prefix="ontokit-lessons-") as temporary:
        packet = Path(temporary) / "packet.json"
        reference = Path(temporary) / "reference.md"
        commands = [
            [python, "-m", "ontology_starterkit.cli", "packs"],
            [python, "-m", "ontology_starterkit.cli", "validate", "examples/hello-ontology"],
            [python, "-m", "ontology_starterkit.cli", "query", "examples/hello-ontology", "manager"],
            [python, "-m", "ontology_starterkit.cli", "eval", "examples/hello-ontology", "manager"],
            [python, "scripts/run_extraction_lesson.py", "examples/life-science-annotations/extraction-lesson.yaml"],
            [python, "scripts/reconcile_business_ids.py", "examples/business-projects/identity-reconciliation.yaml"],
            [python, "scripts/build_decision_packet.py", "examples/consulting-evidence-room", str(packet)],
            [python, "scripts/calculate_roi.py", "docs/for-product-managers/roi-calculator/scenarios.json"],
            [python, "scripts/check_migration.py", "docs/migrations/0.2-to-0.3.yaml", "--query", "manager", "--query", "owner", "--query", "evidence"],
            [python, "scripts/generate_reference.py", "examples/hello-ontology/ontology.ttl", str(reference)],
        ]
        results: list[dict[str, object]] = []
        for command in commands:
            completed = subprocess.run(command, cwd=root, capture_output=True, text=True)
            result = {"command": " ".join(command), "returncode": completed.returncode}
            if completed.returncode:
                result["stderr"] = completed.stderr[-1000:]
                raise RuntimeError(json.dumps(result))
            results.append(result)
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path("."))
    args = parser.parse_args()
    print(json.dumps({"commands": verify(args.repo), "count": 10}, indent=2))


if __name__ == "__main__":
    main()
