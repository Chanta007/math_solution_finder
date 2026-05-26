#!/usr/bin/env python3
"""Append a convergence log entry (JSONL) to docs/convergence/.

Standalone script — stdlib only. Schema matches docs/design/convergence-tracking.md.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REQUIRED_FIELDS = ("run_id", "iteration", "strategy", "result", "confidence", "findings")
VALID_RESULTS = ("solved", "progress", "dead_end", "error")


def build_entry(args: argparse.Namespace) -> dict:
    now = datetime.now(timezone.utc).isoformat()
    problem_hash = ""
    if args.problem:
        problem_hash = "sha256:" + hashlib.sha256(args.problem.encode()).hexdigest()[:16]

    entry = {
        "run_id": args.run_id,
        "iteration": args.iteration,
        "timestamp": now,
        "problem_hash": problem_hash,
        "strategy": args.strategy,
        "approach": args.approach or "",
        "result": args.result,
        "confidence": args.confidence,
        "findings": args.findings,
        "dead_ends": json.loads(args.dead_ends) if args.dead_ends else [],
        "tokens_used": args.tokens_used,
        "cost_usd": args.cost_usd,
        "duration_s": args.duration_s,
        "parent_iteration": args.parent_iteration,
        "path_id": args.path_id or "",
    }
    return entry


def validate_entry(entry: dict) -> list[str]:
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in entry or entry[field] is None:
            errors.append(f"Missing required field: {field}")
    if entry.get("result") not in VALID_RESULTS:
        errors.append(f"Invalid result: {entry.get('result')} (must be one of {VALID_RESULTS})")
    conf = entry.get("confidence", -1)
    if not (0.0 <= conf <= 1.0):
        errors.append(f"Confidence must be 0.0-1.0, got {conf}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Append a convergence log entry (JSONL)")
    parser.add_argument("--run-id", required=True, help="Unique run identifier")
    parser.add_argument("--iteration", type=int, required=True, help="Iteration number")
    parser.add_argument("--strategy", required=True, help="Strategy name")
    parser.add_argument("--result", required=True, choices=VALID_RESULTS, help="Result status")
    parser.add_argument("--confidence", type=float, required=True, help="Confidence score 0.0-1.0")
    parser.add_argument("--findings", required=True, help="Key findings text")
    parser.add_argument("--approach", default="", help="Approach description")
    parser.add_argument("--dead-ends", default="", help="JSON array of dead-end approaches")
    parser.add_argument("--tokens-used", type=int, default=0, help="Tokens consumed")
    parser.add_argument("--cost-usd", type=float, default=0.0, help="Estimated cost")
    parser.add_argument("--duration-s", type=float, default=0.0, help="Duration in seconds")
    parser.add_argument("--parent-iteration", type=int, default=0, help="Parent iteration number")
    parser.add_argument("--path-id", default="", help="Solution path identifier")
    parser.add_argument("--problem", default="", help="Problem description (hashed for ID)")
    parser.add_argument("--log-dir", default="docs/convergence", help="Log directory")

    args = parser.parse_args(argv)
    entry = build_entry(args)

    errors = validate_entry(entry)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    log_dir = Path(args.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"run-{args.run_id}.jsonl"

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    print(json.dumps({"status": "logged", "file": str(log_file), "iteration": args.iteration}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
