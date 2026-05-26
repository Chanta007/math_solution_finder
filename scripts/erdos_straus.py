#!/usr/bin/env python3
"""Erdős–Straus conjecture computation: find x,y,z such that 4/n = 1/x + 1/y + 1/z.

Standalone script — no external dependencies beyond stdlib + sympy.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from typing import Optional


def find_decomposition(n: int, bound: int = 10000) -> Optional[tuple[int, int, int]]:
    """Find positive integers x,y,z such that 4/n = 1/x + 1/y + 1/z.

    Uses greedy decomposition followed by systematic search.
    Returns (x, y, z) with x <= y <= z, or None if not found within bound.
    """
    if n < 2:
        return None

    for x in range(max(1, (n + 3) // 4), bound + 1):
        remainder_num = 4 * x - n
        remainder_den = n * x
        if remainder_num <= 0:
            continue

        for y in range(x, bound + 1):
            num = remainder_num * y - remainder_den
            den = remainder_den * y
            if num <= 0:
                continue
            if den % num == 0:
                z = den // num
                if z >= y:
                    return (x, y, z)
            if num > den:
                break

    return None


def verify_solution(n: int, x: int, y: int, z: int) -> bool:
    """Verify that 4/n = 1/x + 1/y + 1/z exactly using integer arithmetic."""
    if any(v <= 0 for v in (n, x, y, z)):
        return False
    lhs = 4 * x * y * z
    rhs = n * (y * z + x * z + x * y)
    return lhs == rhs


def residue_class_mod_840(n: int) -> dict:
    """Analyze n's residue class mod 840 for Erdős–Straus tractability."""
    r = n % 840
    hard_residues = {1, 121, 169, 289, 361, 529}
    is_hard = r in hard_residues
    return {
        "n": n,
        "residue_mod_840": r,
        "is_hard_residue": is_hard,
        "is_prime": _is_prime(n),
        "congruence_mod_4": n % 4,
    }


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


def scan_range(start: int, end: int, bound: int = 10000) -> dict:
    """Test all n in [start, end] and return statistics."""
    solved = []
    unsolved = []
    t0 = time.time()

    for n in range(start, end + 1):
        result = find_decomposition(n, bound)
        if result is not None:
            solved.append(n)
        else:
            unsolved.append(n)

    elapsed = time.time() - t0
    return {
        "range": [start, end],
        "total": end - start + 1,
        "solved": len(solved),
        "unsolved_count": len(unsolved),
        "unsolved_values": unsolved[:50],
        "solve_rate": len(solved) / (end - start + 1) if end >= start else 0,
        "bound_used": bound,
        "elapsed_seconds": round(elapsed, 3),
    }


def analyze_n(n: int, bound: int = 10000) -> dict:
    """Full analysis of a single n value."""
    residue = residue_class_mod_840(n)
    solution = find_decomposition(n, bound)
    result = {
        **residue,
        "bound_used": bound,
        "solution_found": solution is not None,
    }
    if solution:
        x, y, z = solution
        result["solution"] = {"x": x, "y": y, "z": z}
        result["verified"] = verify_solution(n, x, y, z)
        result["equation"] = f"4/{n} = 1/{x} + 1/{y} + 1/{z}"
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Erdős–Straus conjecture: find x,y,z such that 4/n = 1/x + 1/y + 1/z"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("check", help="Check a single n value")
    p_check.add_argument("n", type=int, help="Value of n (>= 2)")
    p_check.add_argument("--bound", type=int, default=10000, help="Search upper bound")

    p_range = sub.add_parser("range", help="Scan a range of n values")
    p_range.add_argument("start", type=int, help="Start of range")
    p_range.add_argument("end", type=int, help="End of range")
    p_range.add_argument("--bound", type=int, default=10000, help="Search upper bound")

    p_analyze = sub.add_parser("analyze", help="Full analysis of a single n")
    p_analyze.add_argument("n", type=int, help="Value of n (>= 2)")
    p_analyze.add_argument("--bound", type=int, default=10000, help="Search upper bound")

    args = parser.parse_args(argv)

    if args.command == "check":
        result = find_decomposition(args.n, args.bound)
        if result:
            x, y, z = result
            verified = verify_solution(args.n, x, y, z)
            print(json.dumps({
                "n": args.n,
                "solved": True,
                "solution": {"x": x, "y": y, "z": z},
                "verified": verified,
                "equation": f"4/{args.n} = 1/{x} + 1/{y} + 1/{z}",
            }, indent=2))
            return 0
        else:
            print(json.dumps({
                "n": args.n,
                "solved": False,
                "bound_used": args.bound,
            }, indent=2))
            return 3

    elif args.command == "range":
        result = scan_range(args.start, args.end, args.bound)
        print(json.dumps(result, indent=2))
        return 0 if result["unsolved_count"] == 0 else 3

    elif args.command == "analyze":
        result = analyze_n(args.n, args.bound)
        print(json.dumps(result, indent=2))
        return 0 if result["solution_found"] else 3

    return 0


if __name__ == "__main__":
    sys.exit(main())
