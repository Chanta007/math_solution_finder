"""Tests for scripts/theory_state.py — I/O and schema validation only."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def run_state(*args: str, state_dir: str | None = None) -> tuple[int, str, str]:
    env = os.environ.copy()
    result = subprocess.run(
        [sys.executable, "scripts/theory_state.py", *args],
        capture_output=True, text=True,
        cwd=state_dir if state_dir else None,
    )
    return result.returncode, result.stdout, result.stderr


def test_init_creates_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        docs = Path(tmpdir) / "docs"
        docs.mkdir()
        # Copy the script to tmpdir and run from there
        import shutil
        scripts_dir = Path(tmpdir) / "scripts"
        scripts_dir.mkdir()
        shutil.copy("scripts/theory_state.py", scripts_dir / "theory_state.py")

        result = subprocess.run(
            [sys.executable, str(scripts_dir / "theory_state.py"), "init",
             "--problem", "Test problem", "--domain", "math"],
            capture_output=True, text=True, cwd=tmpdir,
        )
        assert result.returncode == 0
        state_file = docs / "theory-state.json"
        assert state_file.exists()
        state = json.loads(state_file.read_text())
        assert state["problem"] == "Test problem"
        assert state["domain"] == "math"
        assert state["confidence"] == 0.0
        assert state["iteration"] == 0


def test_show_displays_state():
    code, out, _ = run_state("show")
    assert code == 0
    state = json.loads(out)
    assert "problem" in state
    assert "confidence" in state


def test_update_increments_iteration():
    code1, out1, _ = run_state("show")
    initial = json.loads(out1)
    initial_iter = initial.get("iteration", 0)

    run_state("update", "--confidence", "0.6", "--findings", "New finding", "--approach", "new-approach")

    code2, out2, _ = run_state("show")
    updated = json.loads(out2)
    assert updated["iteration"] == initial_iter + 1
    assert updated["confidence"] == 0.6


def test_add_evidence():
    run_state("add-evidence", "--source", "test-paper", "--type", "supports", "--summary", "Confirms X")
    code, out, _ = run_state("show")
    state = json.loads(out)
    assert any(e["source"] == "test-paper" for e in state["evidence"])


def test_add_dead_end():
    run_state("add-dead-end", "--approach", "bad-idea", "--reason", "Doesn't work because Y")
    code, out, _ = run_state("show")
    state = json.loads(out)
    assert any(d["approach"] == "bad-idea" for d in state["dead_ends"])


def test_history():
    code, out, _ = run_state("history")
    assert code == 0
    hist = json.loads(out)
    assert "iterations" in hist
    assert "approaches_tried" in hist
