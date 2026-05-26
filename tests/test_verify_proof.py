"""Tests for scripts/verify_proof.py"""
import json
import subprocess
import sys


def run_script(*args: str) -> tuple[int, dict]:
    result = subprocess.run(
        [sys.executable, "scripts/verify_proof.py", *args],
        capture_output=True, text=True,
    )
    output = json.loads(result.stdout) if result.stdout.strip() else {}
    return result.returncode, output


def test_identity_valid():
    code, out = run_script("identity", "--n", "5", "--x", "2", "--y", "4", "--z", "20")
    assert code == 0
    assert out["verified"] is True


def test_identity_another_valid():
    code, out = run_script("identity", "--n", "5", "--x", "2", "--y", "5", "--z", "10")
    assert code == 0
    assert out["verified"] is True


def test_identity_invalid():
    code, out = run_script("identity", "--n", "5", "--x", "2", "--y", "3", "--z", "10")
    assert code == 1
    assert out["verified"] is False


def test_identity_n3():
    code, out = run_script("identity", "--n", "3", "--x", "1", "--y", "4", "--z", "12")
    assert code == 0
    assert out["verified"] is True


def test_residue_hard_case():
    code, out = run_script("residue", "1681")
    assert code == 0
    assert out["is_hard_residue"] is True
    assert out["residue_mod_840"] == 1


def test_residue_easy_case():
    code, out = run_script("residue", "12")
    assert code == 0
    assert out["is_hard_residue"] is False
    assert out["congruence_mod_4"] == 0


def test_parametric_even_n():
    code, out = run_script(
        "parametric",
        "--fx", "n // 2",
        "--fy", "n",
        "--fz", "n",
        "--start", "2",
        "--end", "100",
    )
    # This formula only works for even n, so expect ~50% success for range 2-100
    assert out["tested"] == 99
    assert out["verified"] >= 49  # at least the even values
