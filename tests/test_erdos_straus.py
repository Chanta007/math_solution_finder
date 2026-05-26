"""Tests for scripts/erdos_straus.py"""
import json
import subprocess
import sys


def run_script(*args: str) -> tuple[int, dict]:
    result = subprocess.run(
        [sys.executable, "scripts/erdos_straus.py", *args],
        capture_output=True, text=True,
    )
    output = json.loads(result.stdout) if result.stdout.strip() else {}
    return result.returncode, output


def test_check_known_solution_n5():
    code, out = run_script("check", "5")
    assert code == 0
    assert out["solved"] is True
    assert out["verified"] is True
    x, y, z = out["solution"]["x"], out["solution"]["y"], out["solution"]["z"]
    assert 4 * x * y * z == 5 * (y * z + x * z + x * y)


def test_check_known_solution_n3():
    code, out = run_script("check", "3")
    assert code == 0
    assert out["solved"] is True
    assert out["verified"] is True


def test_check_n2():
    code, out = run_script("check", "2")
    assert code == 0
    assert out["solved"] is True


def test_range_small():
    code, out = run_script("range", "2", "50")
    assert code == 0
    assert out["solved"] == out["total"]
    assert out["solve_rate"] == 1.0


def test_analyze_prime():
    code, out = run_script("analyze", "7")
    assert code == 0
    assert out["is_prime"] is True
    assert out["solution_found"] is True
    assert out["verified"] is True


def test_analyze_hard_residue():
    code, out = run_script("analyze", "1681")
    assert out["residue_mod_840"] == 1
    assert out["is_hard_residue"] is True
