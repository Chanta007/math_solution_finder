"""Tests for scripts/convergence_scorer.py — mechanical metrics only."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run_scorer(*args: str) -> tuple[int, dict]:
    result = subprocess.run(
        [sys.executable, "scripts/convergence_scorer.py", *args],
        capture_output=True, text=True,
    )
    output = json.loads(result.stdout) if result.stdout.strip() else {}
    return result.returncode, output


def _write_entries(tmpdir: str, entries: list[dict]) -> str:
    f = Path(tmpdir) / "run-test.jsonl"
    f.write_text("\n".join(json.dumps(e) for e in entries) + "\n")
    return str(f)


def test_empty_log():
    with tempfile.TemporaryDirectory() as tmpdir:
        f = Path(tmpdir) / "run-empty.jsonl"
        f.write_text("")
        code, out = run_scorer("--log", str(f))
        assert code == 0
        assert out["iterations_completed"] == 0
        assert out["plateau_detected"] is False


def test_single_entry():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = _write_entries(tmpdir, [
            {"confidence": 0.5, "result": "progress", "strategy": "sym", "findings": "found something"}
        ])
        code, out = run_scorer("--log", path)
        assert code == 0
        assert out["iterations_completed"] == 1
        assert out["latest_confidence"] == 0.5
        assert out["progress_count"] == 1


def test_plateau_detection():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = _write_entries(tmpdir, [
            {"confidence": 0.5, "result": "progress", "strategy": "a", "findings": ""},
            {"confidence": 0.5, "result": "progress", "strategy": "b", "findings": ""},
            {"confidence": 0.51, "result": "progress", "strategy": "c", "findings": ""},
        ])
        code, out = run_scorer("--log", path, "--window", "3")
        assert code == 0
        assert out["plateau_detected"] is True


def test_no_verdict_key():
    """Verify the scorer outputs metrics only — no verdict or recommendation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        path = _write_entries(tmpdir, [
            {"confidence": 0.5, "result": "progress", "strategy": "a", "findings": "x"}
        ])
        _, out = run_scorer("--log", path)
        assert "verdict" not in out
        assert "recommendation" not in out
        assert "decision" not in out


def test_existing_log():
    code, out = run_scorer("--log", "docs/convergence/run-proof-erdos-straus-001.jsonl")
    assert code == 0
    assert out["iterations_completed"] == 1
    assert out["latest_strategy"] == "proof-by-residue-cases"


def test_directory_scan():
    code, out = run_scorer("--log", "docs/convergence/")
    assert code == 0
    assert out["iterations_completed"] >= 1
