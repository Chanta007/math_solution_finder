# Proof Strategies for Erdős–Straus Hard Residue Classes

**Predecessor**: [docs/research/2026-05-25-unsolved-math-test-cases.md](2026-05-25-unsolved-math-test-cases.md)

**Date**: 2026-05-26
**Slug**: erdos-straus-hard-residue-proofs
**Status**: approved

---

## Question

Which proof strategy should solver iteration 2 attempt for the 6 hard Erdős–Straus residue classes {1, 121, 169, 289, 361, 529} mod 840? All are n ≡ 1 (mod 4). Iteration 1 solved even n and n ≡ 3 (mod 4) but identified these as the remaining hard cases. The strategy must be implementable as Claude reasoning + Python verification scripts.

## Thinking — How We Got Here

### Initial framing & gut intuition

After iteration 1, the natural next step seemed to be extending Mordell's polynomial identity approach to cover more residue classes. However, Mordell himself proved a fundamental barrier: polynomial identities can only cover non-quadratic-residue classes. Since 1 is always a quadratic residue mod any prime, no finite set of modular polynomial identities can complete the proof. This means the solution MUST use a different technique.

### Pivots during research

Three key pivots:
1. **Mordell's barrier is real** — polynomial identity approaches are provably insufficient. Any solution must go beyond classical modular methods.
2. **Guo (2025) claims a constructive proof** via Method ED2: the identity (4b-1)(4c-1) = 4Pδ+1 with δ|bc. If correct, this resolves the conjecture for all primes p ≡ 1 (mod 4). The paper is on arXiv but unreviewed.
3. **Bradford's one-dimensional reduction** — the conjecture reduces to finding a single valid (x,d) pair per prime, with x in [⌈p/4⌉, ⌈p/2⌉]. This gives us a practical verification framework independent of any particular proof strategy.

### Options we considered and rejected

No options were outright rejected — all four have merit. However:
- Pure brute-force (original erdos_straus.py approach) is insufficient for proof — it finds solutions but doesn't prove they exist for all n.
- Analytic methods (Elsholtz-Tao framework) face a structural obstruction: f(p) grows only polylogarithmically, making counting arguments alone insufficient.

### Open empirical questions deliberately not answered here

1. **Is Guo's proof correct?** The paper claims Theorem 10.21 resolves the conjecture for all primes p ≡ 1 (mod 4), but it hasn't been peer-reviewed. Our iteration will test its core identity computationally for specific primes — if it fails for any prime, we have a concrete counterexample to the paper's claim.
2. **How efficient is Guo's construction in practice?** The triple (δ, b, c) must be "constructed explicitly" but the paper's algorithm may require searching over divisors of bc. We don't know the practical complexity until we implement it.
3. **Does Mordell's barrier apply to Guo's approach?** Guo's method uses algebraic factorization, not modular polynomial identities — it may legitimately circumvent the barrier. But this needs verification.
4. Adversarial check: searched for retractions/errors in Guo 2025; no counter-evidence found in top results. Caveat: unreviewed preprint.

## Options Considered

| Option | Pros | Cons | Cost |
|--------|------|------|------|
| **A. Guo's Method ED2** | Claims complete proof for p≡1(mod 4); explicit construction via (4b-1)(4c-1)=4Pδ+1; bypasses Mordell's barrier by using algebraic factorization, not modular identities | Unverified preprint (2025); may have errors; requires understanding the full triple (δ,b,c) construction | Medium — implement identity, test on hard primes |
| **B. Azarian's parametric** | Unified framework; density-one coverage proven via Dirichlet series; explicit formulas when n has divisor b≡3(mod 4) | Doesn't cover primes p≡1(mod 4) without b≡3(mod 4) divisors (density zero but infinite); heavy analytic machinery | Medium — implement F_{x,t} function, test perfect-square detection |
| **C. Bradford's Type I/II search** | One-dimensional reduction; practical; well-documented (published 2025 in INTEGERS); computable | No polynomial-time guarantee for hard residues; empirical search, not a proof; finds solutions but doesn't prove existence | Small — implement (x,d) search per prime |
| **D. Deng's congruence system** | Complete congruence system claimed; Type A+B framework; verified for first 10,000 primes | Conjecture 1 is itself unproven; requires exhaustive check per prime; no density guarantee | Medium — implement congruence checking |

## Decision + Rationale

**Recommended: Option A (Guo's Method ED2) + Option C (Bradford's search) as verification fallback.**

Guo's 2025 paper claims the strongest result — a constructive proof that for every prime P ≡ 1 (mod 4), the decomposition 4/P = 1/A + 1/(bP) + 1/(cP) exists, where A = bc/δ and (4b-1)(4c-1) = 4Pδ+1. Even if the full proof has gaps, implementing the core identity and testing it computationally for specific hard primes (those in the 6 residue classes mod 840) is the highest-value iteration. Bradford's Type I/II framework provides an independent verification method — if Guo's construction produces a valid (x,y,z) triple, Bradford's one-dimensional search should also find it.

The key insight from the research is Mordell's barrier theorem: no finite set of polynomial identities can complete the proof, because 1 is always a quadratic residue. This means we need algebraic (not just modular) techniques. Guo's factorization identity (4b-1)(4c-1) = 4Pδ+1 is algebraic — it operates on the multiplicative structure of the integers, not on residue classes. Whether it actually works is an empirical question our solver iteration will answer.

## Evidence

### External

**Guo (2025)**: "Method ED2 yields the central identity (4b-1)(4c-1) = 4Pδ+1, where δ divides bc, A = bc/δ, B = bP, C = cP. The resulting decomposition is 4/P = 1/A + 1/(bP) + 1/(cP)." (arXiv:2511.07465)

**Mordell (1967)**: Polynomial identities cover all n except residues {1, 121, 169, 289, 361, 529} mod 840. "A polynomial identity for n ≡ r (mod p) can exist only when r is not a quadratic residue modulo p." (via Wikipedia)

**Elsholtz & Tao (2011)**: "N log² N ≪ Σ f(p) ≪ N log² N log log N. The slower-than-polynomial growth creates a serious obstruction to solution by analytic methods." (arXiv:1107.1010)

**Bradford (2025)**: "Reduces the conjecture to a one-dimensional search for a single valid (x,d) pair per prime." Published in INTEGERS journal. (arXiv:2403.16047, published as #A54 INTEGERS 25)

**Azarian (2026)**: "Integers n ≡ 1 (mod 4) without prime divisors ≡ 3 (mod 4) have natural density zero." Proves density-one coverage. (arXiv:2602.20036v2)

**Salez (2014)**: Seven-equation sieve verifying to 10^17. "A C++ program allows checking from a few minutes for N=10^14 to about 16 hours for N=10^17." (arXiv:1406.6307)

**Mihnea & Dumitru (2025)**: Extended verification to 10^18 using modular filtering with prime filters up to S_29. (arXiv:2509.00128)

**Grigore (2025)**: "Four polynomial families. Computational verification to 10^9 confirms every integer of form 4q+1 arises from at least one family." (arXiv:2508.07383v1)

**Deng (2024)**: "Conjecture 1 asserts every prime satisfies at least one congruence condition. Verified for first 10,000 primes." (arXiv:2404.01508v3)

### Internal patterns referenced

- `docs/convergence/run-proof-erdos-straus-001.jsonl`: iteration 1 findings (confidence 0.4, strategy "proof-by-residue-cases", dead end: Schinzel formula gives 3/n not 4/n)
- `scripts/verify_proof.py`: identity verification (exact rational arithmetic), residue analysis, parametric formula testing
- `scripts/erdos_straus.py`: brute-force search + residue classification (for sanity-checking proof claims)

### Source tensions

1. **Mordell barrier vs. Guo claim**: Mordell proved polynomial identities cannot cover quadratic-residue classes. Guo claims to resolve p ≡ 1 (mod 4) via algebraic factorization. If Guo is correct, the method circumvents the barrier; if wrong, the barrier stands.
2. **Analytic obstruction vs. algebraic progress**: Elsholtz-Tao show polylogarithmic growth obstructs analytic methods. But multiple 2025-2026 papers (Guo, Grigore, Azarian) report algebraic progress that doesn't rely on counting arguments.

## Parked Future Angles

- **Azarian's unified parametric framework**: covers density-one but not all primes. *Revisit when:* Guo's method fails for specific primes p ≡ 1 (mod 4) — Azarian may cover those via divisor arguments.
- **Deng's congruence system (Type A+B)**: systematic but unproven. *Revisit when:* Bradford search optimization is needed — Deng's congruence conditions may reduce the search space.
- **Elsholtz-Tao analytic bounds + Cayley surface interpretation**: deep geometric framework. *Revisit when:* algebraic approaches exhaust their capacity and we need to understand the geometric structure of the solution space.
- **Grigore's four polynomial families**: verified to 10^9. *Revisit when:* Guo's method needs a fallback for specific hard primes — Grigore's families may cover some of them.

## Re-evaluation Hooks

1. **If Guo's Method ED2 fails for any prime p ≡ 1 (mod 4)**: reopen this research — the core recommended strategy would be invalidated. Switch to Azarian + Bradford combination.
2. **If Guo's paper is retracted or a specific error is identified**: immediately switch to Bradford (Option C) as primary, with Deng (Option D) as secondary.
