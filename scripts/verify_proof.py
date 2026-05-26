#!/usr/bin/env python3
"""Verify algebraic proof claims for Erdős–Straus conjecture.

Standalone script — stdlib + sympy. Used to VERIFY proof steps, not search for solutions.
"""
from __future__ import annotations

import argparse
import json
import sys
from fractions import Fraction


def verify_identity(n: int, x: int, y: int, z: int) -> dict:
    """Verify that 4/n = 1/x + 1/y + 1/z using exact rational arithmetic."""
    if any(v <= 0 for v in (n, x, y, z)):
        return {"verified": False, "error": "All values must be positive integers"}

    lhs = Fraction(4, n)
    rhs = Fraction(1, x) + Fraction(1, y) + Fraction(1, z)
    verified = lhs == rhs

    return {
        "verified": verified,
        "n": n, "x": x, "y": y, "z": z,
        "lhs": str(lhs),
        "rhs": str(rhs),
        "equation": f"4/{n} = 1/{x} + 1/{y} + 1/{z}",
    }


def analyze_residue(n: int) -> dict:
    """Analyze n's residue class mod 840 and list known parametric solutions."""
    r = n % 840
    hard_residues = {1, 121, 169, 289, 361, 529}
    is_hard = r in hard_residues

    parametric = _get_parametric_solutions(n, r)

    return {
        "n": n,
        "residue_mod_840": r,
        "is_hard_residue": is_hard,
        "is_prime": _is_prime(n),
        "congruence_mod_4": n % 4,
        "congruence_mod_3": n % 3,
        "known_parametric_solutions": parametric,
        "coverage": "covered" if parametric else ("hard_case" if is_hard else "standard_greedy"),
    }


def _get_parametric_solutions(n: int, r: int) -> list[dict]:
    """Return known parametric solutions that apply to this n."""
    solutions = []

    if n % 4 == 0:
        k = n // 4
        solutions.append({
            "name": "n ≡ 0 (mod 4)",
            "formula": f"4/{n} = 1/{k} + 1/{k} + ... (trivial: 4/{n} = 1/{n//4})",
            "x": k, "y": n, "z": n * k,
            "proof": "If 4|n, then 4/n = 1/(n/4), decompose remainder"
        })

    if n % 4 == 2:
        k = (n + 2) // 4
        if (n + 2) % 4 == 0:
            x_val = k
            remainder_num = 4 * x_val - n
            remainder_den = n * x_val
            if remainder_num > 0 and remainder_den % remainder_num == 0:
                pass

    if n % 4 == 3:
        x_val = (n + 1) // 4
        if (n + 1) % 4 == 0:
            remainder = Fraction(4, n) - Fraction(1, x_val)
            if remainder > 0:
                solutions.append({
                    "name": "n ≡ 3 (mod 4)",
                    "formula": f"x = (n+1)/4 = {x_val}, then decompose remainder {remainder}",
                    "approach": "greedy_first_term",
                })

    if n % 3 == 0:
        solutions.append({
            "name": "n ≡ 0 (mod 3)",
            "formula": f"4/{n} = 1/{n} + 1/{n} + 2/{n} = 1/{n} + 1/{n} + 1/{n//2} (if 2|n)",
            "approach": "divisibility_by_3",
        })

    return solutions


def test_parametric_formula(formula_x: str, formula_y: str, formula_z: str,
                            start: int, end: int) -> dict:
    """Test a parametric formula x(n), y(n), z(n) over a range of n values."""
    results = {"tested": 0, "verified": 0, "failed": [], "formula": {
        "x": formula_x, "y": formula_y, "z": formula_z,
    }}

    for n in range(start, end + 1):
        try:
            x = eval(formula_x, {"n": n, "__builtins__": {"int": int, "max": max, "min": min, "abs": abs}})
            y = eval(formula_y, {"n": n, "__builtins__": {"int": int, "max": max, "min": min, "abs": abs}})
            z = eval(formula_z, {"n": n, "__builtins__": {"int": int, "max": max, "min": min, "abs": abs}})

            if not all(isinstance(v, int) and v > 0 for v in (x, y, z)):
                results["failed"].append({"n": n, "reason": "non-positive integer"})
                results["tested"] += 1
                continue

            check = verify_identity(n, x, y, z)
            results["tested"] += 1
            if check["verified"]:
                results["verified"] += 1
            else:
                results["failed"].append({"n": n, "x": x, "y": y, "z": z, "reason": "identity_failed"})
        except Exception as e:
            results["failed"].append({"n": n, "reason": str(e)})
            results["tested"] += 1

    results["success_rate"] = results["verified"] / results["tested"] if results["tested"] > 0 else 0
    results["failed"] = results["failed"][:20]
    return results


def _is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify algebraic proof claims for Erdős–Straus conjecture"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_id = sub.add_parser("identity", help="Verify a specific (n, x, y, z) identity")
    p_id.add_argument("--n", type=int, required=True)
    p_id.add_argument("--x", type=int, required=True)
    p_id.add_argument("--y", type=int, required=True)
    p_id.add_argument("--z", type=int, required=True)

    p_res = sub.add_parser("residue", help="Analyze residue class and known solutions")
    p_res.add_argument("n", type=int, help="Value to analyze")

    p_param = sub.add_parser("parametric", help="Test a parametric formula over a range")
    p_param.add_argument("--fx", required=True, help="Formula for x as function of n")
    p_param.add_argument("--fy", required=True, help="Formula for y as function of n")
    p_param.add_argument("--fz", required=True, help="Formula for z as function of n")
    p_param.add_argument("--start", type=int, default=2, help="Start of range")
    p_param.add_argument("--end", type=int, default=100, help="End of range")

    args = parser.parse_args(argv)

    if args.command == "identity":
        result = verify_identity(args.n, args.x, args.y, args.z)
        print(json.dumps(result, indent=2))
        return 0 if result["verified"] else 1

    elif args.command == "residue":
        result = analyze_residue(args.n)
        print(json.dumps(result, indent=2, default=str))
        return 0

    elif args.command == "parametric":
        result = test_parametric_formula(args.fx, args.fy, args.fz, args.start, args.end)
        print(json.dumps(result, indent=2))
        return 0 if result["success_rate"] == 1.0 else 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
