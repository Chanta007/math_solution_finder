#!/usr/bin/env python3
"""Compute convergence metrics from JSONL logs. Mechanical scoring only — no decisions.

The LLM (via skill/discover/SKILL.md) interprets these metrics and decides
whether to continue, pivot, or stop. This script only computes numbers.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_entries(log_path: str) -> list[dict]:
    p = Path(log_path)
    entries = []
    if p.is_file():
        for line in p.read_text(encoding="utf-8").strip().splitlines():
            if line.strip():
                entries.append(json.loads(line))
    elif p.is_dir():
        for f in sorted(p.glob("run-*.jsonl")):
            for line in f.read_text(encoding="utf-8").strip().splitlines():
                if line.strip():
                    entries.append(json.loads(line))
    return entries


def compute_metrics(entries: list[dict], window: int = 3) -> dict:
    if not entries:
        return {
            "iterations_completed": 0,
            "latest_confidence": 0.0,
            "confidence_trend": [],
            "plateau_detected": False,
            "plateau_length": 0,
            "strategies_tried": [],
            "dead_end_count": 0,
            "progress_count": 0,
            "solved_count": 0,
            "error_count": 0,
            "latest_findings": "",
            "latest_strategy": "",
        }

    confidences = [e.get("confidence", 0.0) for e in entries]
    results = [e.get("result", "") for e in entries]
    strategies = list(dict.fromkeys(e.get("strategy", "") for e in entries))

    plateau_detected = False
    plateau_length = 0
    if len(confidences) >= window:
        recent = confidences[-window:]
        if max(recent) - min(recent) < 0.05:
            plateau_detected = True
            for i in range(len(confidences) - 1, 0, -1):
                if abs(confidences[i] - confidences[i - 1]) >= 0.05:
                    break
                plateau_length += 1
            plateau_length += 1

    return {
        "iterations_completed": len(entries),
        "latest_confidence": confidences[-1] if confidences else 0.0,
        "confidence_trend": confidences,
        "plateau_detected": plateau_detected,
        "plateau_length": plateau_length,
        "strategies_tried": strategies,
        "dead_end_count": results.count("dead_end"),
        "progress_count": results.count("progress"),
        "solved_count": results.count("solved"),
        "error_count": results.count("error"),
        "latest_findings": entries[-1].get("findings", "") if entries else "",
        "latest_strategy": entries[-1].get("strategy", "") if entries else "",
    }


PLACEHOLDER_PATTERNS = ["test-paper", "Confirms X", "bad-idea", "Doesn't work because Y"]


def validate_theory_state(log_entries: list[dict]) -> dict:
    """Check theory-state.json for placeholder data and iteration mismatches."""
    state_file = Path("docs/theory-state.json")
    if not state_file.exists():
        return {"valid": True, "issues": ["theory-state.json not found (skip validation)"]}

    state = json.loads(state_file.read_text(encoding="utf-8"))
    issues = []

    for ev in state.get("evidence", []):
        for field in ("source", "summary"):
            val = ev.get(field, "")
            for pattern in PLACEHOLDER_PATTERNS:
                if pattern.lower() in val.lower():
                    issues.append(f"placeholder evidence: '{val}' matches '{pattern}'")

    for de in state.get("dead_ends", []):
        for field in ("approach", "reason"):
            val = de.get(field, "")
            for pattern in PLACEHOLDER_PATTERNS:
                if pattern.lower() in val.lower():
                    issues.append(f"placeholder dead_end: '{val}' matches '{pattern}'")

    if not state.get("current_theory", "").strip():
        issues.append("current_theory is empty")

    state_iter = state.get("iteration", 0)
    log_count = len(log_entries)
    if log_count > 0 and state_iter > 0 and abs(state_iter - log_count) > 1:
        issues.append(f"iteration mismatch: theory-state={state_iter}, convergence_log={log_count}")

    return {"valid": len(issues) == 0, "issues": issues}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compute convergence metrics from JSONL logs (no decisions — metrics only)"
    )
    parser.add_argument("--log", required=True, help="Path to JSONL file or directory")
    parser.add_argument("--window", type=int, default=3, help="Plateau detection window")
    parser.add_argument("--validate", action="store_true",
                        help="Also validate theory-state.json for placeholder entries")

    args = parser.parse_args(argv)
    entries = load_entries(args.log)
    metrics = compute_metrics(entries, args.window)

    if args.validate:
        metrics["validation"] = validate_theory_state(entries)

    print(json.dumps(metrics, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
