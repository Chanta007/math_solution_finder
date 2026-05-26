#!/usr/bin/env python3
"""Manage theory state (docs/theory-state.json). I/O and schema validation only.

The LLM (via skill/discover/SKILL.md) decides WHAT to write.
This script handles HOW to read/write/validate the file.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = Path("docs/theory-state.json")

SCHEMA_KEYS = {"problem", "domain", "current_theory", "confidence", "evidence", "approaches_tried", "dead_ends", "iteration", "last_updated"}


def _load() -> dict:
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def _save(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def cmd_init(args: argparse.Namespace) -> int:
    state = {
        "problem": args.problem,
        "domain": args.domain,
        "current_theory": "",
        "confidence": 0.0,
        "evidence": [],
        "approaches_tried": [],
        "dead_ends": [],
        "iteration": 0,
        "last_updated": _now(),
    }
    _save(state)
    print(json.dumps({"status": "initialized", "file": str(STATE_FILE)}))
    return 0


def cmd_show(_args: argparse.Namespace) -> int:
    state = _load()
    if not state:
        print(json.dumps({"error": "No theory state found. Run 'init' first."}))
        return 1
    print(json.dumps(state, indent=2, ensure_ascii=False))
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    state = _load()
    if not state:
        print(json.dumps({"error": "No theory state found. Run 'init' first."}), file=sys.stderr)
        return 1

    if args.confidence is not None:
        state["confidence"] = args.confidence
    if args.findings:
        state["current_theory"] = args.findings
    if args.approach:
        if args.approach not in state["approaches_tried"]:
            state["approaches_tried"].append(args.approach)
    state["iteration"] = state.get("iteration", 0) + 1
    state["last_updated"] = _now()
    _save(state)
    print(json.dumps({"status": "updated", "iteration": state["iteration"]}))
    return 0


def cmd_add_evidence(args: argparse.Namespace) -> int:
    state = _load()
    if not state:
        print(json.dumps({"error": "No theory state found. Run 'init' first."}), file=sys.stderr)
        return 1

    entry = {
        "source": args.source,
        "type": args.type,
        "summary": args.summary,
        "iteration": state.get("iteration", 0),
        "timestamp": _now(),
    }
    state["evidence"].append(entry)
    state["last_updated"] = _now()
    _save(state)
    print(json.dumps({"status": "evidence_added", "total_evidence": len(state["evidence"])}))
    return 0


def cmd_add_dead_end(args: argparse.Namespace) -> int:
    state = _load()
    if not state:
        print(json.dumps({"error": "No theory state found. Run 'init' first."}), file=sys.stderr)
        return 1

    state["dead_ends"].append({
        "approach": args.approach,
        "reason": args.reason,
        "iteration": state.get("iteration", 0),
    })
    state["last_updated"] = _now()
    _save(state)
    print(json.dumps({"status": "dead_end_added", "total_dead_ends": len(state["dead_ends"])}))
    return 0


def cmd_history(_args: argparse.Namespace) -> int:
    state = _load()
    if not state:
        print(json.dumps({"error": "No theory state found."}), file=sys.stderr)
        return 1

    print(json.dumps({
        "problem": state.get("problem", ""),
        "iterations": state.get("iteration", 0),
        "confidence": state.get("confidence", 0.0),
        "approaches_tried": state.get("approaches_tried", []),
        "dead_ends_count": len(state.get("dead_ends", [])),
        "evidence_count": len(state.get("evidence", [])),
    }, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Theory state manager (I/O only)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Initialize theory state")
    p_init.add_argument("--problem", required=True)
    p_init.add_argument("--domain", required=True)

    sub.add_parser("show", help="Display current theory state")

    p_upd = sub.add_parser("update", help="Update theory state")
    p_upd.add_argument("--confidence", type=float)
    p_upd.add_argument("--findings", default="")
    p_upd.add_argument("--approach", default="")

    p_ev = sub.add_parser("add-evidence", help="Add evidence item")
    p_ev.add_argument("--source", required=True)
    p_ev.add_argument("--type", required=True, choices=["supports", "contradicts"])
    p_ev.add_argument("--summary", required=True)

    p_de = sub.add_parser("add-dead-end", help="Record a dead end")
    p_de.add_argument("--approach", required=True)
    p_de.add_argument("--reason", required=True)

    sub.add_parser("history", help="Show theory evolution summary")

    args = parser.parse_args(argv)
    commands = {
        "init": cmd_init, "show": cmd_show, "update": cmd_update,
        "add-evidence": cmd_add_evidence, "add-dead-end": cmd_add_dead_end,
        "history": cmd_history,
    }
    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
