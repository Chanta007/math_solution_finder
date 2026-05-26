"""Tests for scripts/log_convergence.py"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run_script(*args: str) -> tuple[int, str, str]:
    result = subprocess.run(
        [sys.executable, "scripts/log_convergence.py", *args],
        capture_output=True, text=True,
    )
    return result.returncode, result.stdout, result.stderr


def test_basic_log_entry():
    with tempfile.TemporaryDirectory() as tmpdir:
        code, out, err = run_script(
            "--run-id", "test-001",
            "--iteration", "1",
            "--strategy", "test-strategy",
            "--result", "progress",
            "--confidence", "0.5",
            "--findings", "Test findings",
            "--log-dir", tmpdir,
        )
        assert code == 0
        log_file = Path(tmpdir) / "run-test-001.jsonl"
        assert log_file.exists()
        entry = json.loads(log_file.read_text().strip())
        assert entry["run_id"] == "test-001"
        assert entry["iteration"] == 1
        assert entry["strategy"] == "test-strategy"
        assert entry["result"] == "progress"
        assert entry["confidence"] == 0.5


def test_schema_has_all_fields():
    with tempfile.TemporaryDirectory() as tmpdir:
        run_script(
            "--run-id", "test-schema",
            "--iteration", "1",
            "--strategy", "s",
            "--result", "solved",
            "--confidence", "1.0",
            "--findings", "found it",
            "--log-dir", tmpdir,
        )
        entry = json.loads((Path(tmpdir) / "run-test-schema.jsonl").read_text().strip())
        required = ["run_id", "iteration", "timestamp", "strategy", "result", "confidence", "findings"]
        for field in required:
            assert field in entry, f"Missing field: {field}"


def test_invalid_result_rejected():
    with tempfile.TemporaryDirectory() as tmpdir:
        code, _, _ = run_script(
            "--run-id", "test-bad",
            "--iteration", "1",
            "--strategy", "s",
            "--result", "invalid_status",
            "--confidence", "0.5",
            "--findings", "x",
            "--log-dir", tmpdir,
        )
        assert code != 0


def test_append_behavior():
    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(3):
            run_script(
                "--run-id", "test-append",
                "--iteration", str(i + 1),
                "--strategy", "s",
                "--result", "progress",
                "--confidence", "0.5",
                "--findings", f"iteration {i+1}",
                "--log-dir", tmpdir,
            )
        lines = (Path(tmpdir) / "run-test-append.jsonl").read_text().strip().split("\n")
        assert len(lines) == 3
