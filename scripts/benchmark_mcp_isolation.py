"""Stress the MCP process boundary and prove timed-out workers are reaped."""

from __future__ import annotations

import argparse
import json
from multiprocessing import active_children
from pathlib import Path
import time

from ontology_starterkit.mcp_server import run_query_tool
from ontology_starterkit.packs import PackError


def benchmark(pack: str | Path, *, iterations: int = 32, timeout_seconds: float = 0.01, worker_delay_seconds: float = 0.1) -> dict[str, object]:
    if iterations < 1:
        raise ValueError("iterations must be positive")
    before = len(active_children())
    peak = before
    timeouts = 0
    started = time.monotonic()
    for _ in range(iterations):
        try:
            run_query_tool(
                pack,
                "manager",
                timeout_seconds=timeout_seconds,
                _worker_delay_seconds=worker_delay_seconds,
            )
        except PackError as exc:
            if "deadline" not in str(exc):
                raise
            timeouts += 1
        peak = max(peak, len(active_children()))
    after = len(active_children())
    return {
        "iterations": iterations,
        "timeouts": timeouts,
        "workers_before": before,
        "workers_peak": peak,
        "workers_after": after,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "no_worker_accumulation": after == before,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pack", type=Path, nargs="?", default=Path("examples/hello-ontology"))
    parser.add_argument("--iterations", type=int, default=32)
    args = parser.parse_args()
    result = benchmark(args.pack, iterations=args.iterations)
    print(json.dumps(result, indent=2))
    if not result["no_worker_accumulation"] or result["timeouts"] != args.iterations:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
