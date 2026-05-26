# Unsolved Math Problems for Agentic Solver Test Cases

**Date**: 2026-05-25
**Slug**: unsolved-math-test-cases
**Status**: approved

---

## Question

Which 3 unsolved math problems (50+ years old) should serve as initial test cases for the Math Solution Finder agentic solver? Requirements: (1) well-defined symbolic/numeric formulations suitable for sympy/numpy, (2) unsolved for 50+ years, (3) varying difficulty to test convergence tracking, (4) partial progress made so an agentic loop might plausibly make incremental progress.

## Thinking — How We Got Here

### Initial framing & gut intuition

The "big four" unsolved problems (Riemann Hypothesis, Goldbach, Twin Primes, Collatz) were the obvious starting candidates. Initial gut said Collatz is ideal for testing (trivially computable) but Riemann is too abstract for a sympy-based solver. Suspected we'd need at least one lesser-known problem with more tractable special cases.

### Pivots during research

Two key pivots:
1. Discovery of the **Erdős–Straus Conjecture** — far more tractable than the big four, with a concrete polynomial Diophantine equation (4xyz = n(xy + xz + yz)) and modular arithmetic reduction to 6 residue classes mod 840. This became the "easy tier" candidate, displacing Twin Primes.
2. Discovery of **FrontierMath** and **HorizonMath** benchmarks — purpose-built for "verification is computationally efficient" problems. Confirmed that the right problem selection prioritizes computable verification over proof elegance.

### Options we considered and rejected

- **Riemann Hypothesis** — too abstract for symbolic/numeric testing. The critical strip zeros can be computed numerically, but connecting computation to proof requires analytic number theory beyond what an agentic loop can generate. Kept as aspirational but not in initial test suite.
- **Twin Prime Conjecture** — the Zhang/Maynard bounded gaps results (gap ≤ 246) are proven, but reducing the gap further requires deep sieve theory. Less gradient of difficulty than Collatz or Erdős–Straus. Parked for future work.
- **Hadamard matrix order 668** — highly tractable (95-99% solvable per FrontierMath) but more of a combinatorial search problem than a conjecture. Doesn't test the "research loop feeding into next iteration" pattern well. Parked.
- **R(5,5) exact Ramsey number** — bounded between 43 and 46, concrete and numeric, but primarily a SAT solver problem. Would require integrating a SAT solver into the strategy registry. Parked until SAT integration exists.

### Open empirical questions deliberately not answered here

1. **Can an LLM-based solver make genuine mathematical progress, or only organize known results?** AlphaProof solved IMO problems (Nature 2025), but no AI has made progress on open conjectures. Our solver uses Claude for approach generation, not proof verification — the sympy/numpy layer handles verification. Whether Claude can generate novel proof strategies (not just recombine known ones) is an empirical question the solver runs will answer.
2. **What convergence patterns will emerge?** We designed the convergence tracking schema (JSONL with confidence scores, path branching) but don't know what actual solver runs will look like. Will confidence plateau quickly? Will dead-end detection work? Only real runs will tell.
3. **Is the difficulty gradient real in practice?** We ordered Erdős–Straus < Collatz < Goldbach based on formulation complexity and literature, but the agentic loop might find different difficulty orderings.

## Options Considered

| Option | Pros | Cons | Cost |
|--------|------|------|------|
| **1. Erdős–Straus Conjecture** (4/n = 1/x + 1/y + 1/z) | Polynomial Diophantine equation, verified to 10^17, reduces to 6 residue classes mod 840, greedy algorithm covers most cases | Less famous — fewer Claude training examples about it; remaining hard cases (primes ≡ 1 mod 4) may be genuinely intractable | Small — straightforward to formulate in sympy |
| **2. Collatz Conjecture** (n/2 or 3n+1) | Trivially computable, verified to 2.36×10^21, Tao's 2019 partial result, Conway undecidability of generalization, excellent for testing path branching | Conway's undecidability result for generalized Collatz suggests fundamental barriers; may produce lots of iterations with no convergence signal | Small — iteration function is trivial to implement |
| **3. Goldbach's Conjecture** (even n = p + q) | Weak conjecture proved (Helfgott 2013), Chen's theorem provides intermediate target, rich literature, well-defined primality testing | Hardest of the three — strong conjecture may be beyond any automated approach; prime decomposition search space grows with n | Medium — primality testing at scale requires optimized algorithms |
| **4. Twin Prime gap bound** (gap → 2) | Current bound 246 (Maynard/Polymath), clear numeric target, strong recent progress | Requires deep sieve theory; less suitable for sympy symbolic approach; gap reduction is technically very hard | Large — sieve methods are complex to implement |

**Recommended**: Options 1 + 2 + 3 as the initial test suite.

## Decision + Rationale

Select **Erdős–Straus + Collatz + Goldbach** as the three test problems, forming a difficulty gradient:

1. **Erdős–Straus** (EASY tier): The polynomial Diophantine formulation (4xyz = n(xy + xz + yz)) maps directly to sympy's equation solver. The modular arithmetic reduction to 6 residue classes mod 840 gives the agentic loop a concrete strategy to follow — try known residue class solutions, then focus on the remaining hard cases. Best for validating the basic solver loop, strategy registry, and convergence logging work correctly.

2. **Collatz** (MEDIUM tier): The iteration function f(n) = n/2 if even, 3n+1 if odd is trivially computable in both sympy and numpy. The open question is about the *structure* of all orbits, not individual computation. This tests the solver's ability to generate and evaluate structural hypotheses — proof by contradiction, induction, probabilistic arguments, orbit analysis. Tao's 2019 "almost all" result (logarithmic density) shows partial proofs are achievable. Best for testing convergence tracking with many iterations, dead-end detection, and path branching.

3. **Goldbach** (HARD tier): Requires the solver to work with prime decomposition, sieve methods, and additive number theory. The weak conjecture (sum of 3 primes) being proved provides a lower bound on what's achievable. Chen's theorem (prime + semiprime) is an intermediate target. Best for testing strategy diversity — the solver should try symbolic approaches (algebraic identity manipulation), numeric approaches (statistical patterns in prime gaps), and hybrid approaches (analytic number theory formulas).

All three have built-in verification: Erdős–Straus checks an equation, Collatz checks orbit termination, Goldbach checks prime sum. This aligns with the `SymbolicStrategy` and `NumericStrategy` in the solver design.

**Adversarial caveat**: LLMs may not be capable of genuinely novel mathematical reasoning — they recombine patterns from training data. This is acknowledged but doesn't invalidate the test suite: the project's primary goal is testing the *harness infrastructure* (convergence tracking, strategy selection, agentic loops, orchestrate/triage integration), not actually solving these conjectures. Any genuine mathematical progress would be a bonus.

## Evidence

### External

**Erdős–Straus Conjecture:**
- Wikipedia (https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93Straus_conjecture): "For every integer n >= 2, there exist positive integers x, y, and z for which 4/n = 1/x + 1/y + 1/z." Verified up to n ≤ 10^17. Counterexamples can only exist among primes ≡ 1, 121, 169, 289, 361, or 529 mod 840.

**Collatz Conjecture:**
- Wikipedia (https://en.wikipedia.org/wiki/Collatz_conjecture): Verified for all positive integers up to 2.36×10^21. Conway (1972) proved generalized version is undecidable.
- Tao (2019, arXiv:1909.03562): "Almost all orbits of the Collatz map attain almost bounded values" — proved for logarithmic density.
- arXiv (2025, arXiv:2502.16743): Verification algorithms work for numbers with up to 10 billion decimal places.

**Goldbach's Conjecture:**
- Wikipedia (https://en.wikipedia.org/wiki/Goldbach's_conjecture): Verified up to n ≤ 4×10^18. Chen's theorem (1973): every sufficiently large even number = prime + semiprime. Helfgott (2013) proved weak conjecture.
- ScienceDirect: GPU-accelerated verification frameworks (GoldbachGPU) push computational limits.

**AI/LLM Math Capability:**
- Nature (2025): AlphaProof solved 3 IMO problems including P6 (hardest, solved by only 5/609 humans). Uses neural networks + Lean symbolic engine.
- Scientific American (2024): Guth & Maynard improved Ingham bound on Riemann zeros — first progress in 50+ years, done by humans not AI.
- FrontierMath (https://epoch.ai/frontiermath/open-problems): Benchmark of 14 unsolved problems curated for automated solving. GPT 5.4 Pro improved best-known results on 2 problems.
- HorizonMath (arXiv:2603.15617): 100+ unsolved problems "where discovery is hard but verification is computationally efficient."

### Internal patterns referenced

- `Problem` type (`src/math_solver/types/problem.py`) — represents problem with description, category, formulation
- `ConvergenceEntry` type (`src/math_solver/types/convergence.py`) — tracks approach, strategy, result, confidence per iteration
- `StrategyRegistry` (`src/math_solver/strategies/registry.py`) — pluggable strategy selection
- `SymbolicStrategy` / `NumericStrategy` — sympy and numpy verification strategies
- `Solver.run_loop()` — main agentic iteration orchestrator
- `ConvergenceDetector` — detects convergence via solution, plateau, exhaustion, or limit
- `create_llm_client()` factory — wraps Anthropic SDK with rate limiting
- Dependency layers (CONSTRAINTS §3): CLI → Engine → Strategies → Math Core → Infrastructure
- Convergence logging (CONSTRAINTS §7.1): append-only JSONL, never edit or delete

### Source tensions

1. **AI math capability**: AlphaProof (Nature 2025) solved IMO P6, suggesting AI can handle hard math. But no AI has made progress on open conjectures. FrontierMath/HorizonMath benchmarks are designed specifically for problems where "verification is efficient" — implying current AI is better at search + verify than at proof generation.
2. **Collatz tractability**: Tao's 2019 result proves "almost all" orbits converge, but Conway's 1972 result proves the generalized version is undecidable. Tension: does Tao's partial progress suggest the specific Collatz conjecture is provable, or does Conway's result indicate fundamental barriers?

## Parked Future Angles

- **Twin Prime gap reduction** (gap ≤ 246 → gap = 2). *Revisit when:* solver handles sieve-method strategy and can express Maynard's GPY weight optimization in sympy.
- **Hadamard matrix order 668**. *Revisit when:* solver supports matrix construction strategies and SAT solver integration (95-99% solvable per FrontierMath).
- **Ramsey number R(5,5)** (bounded 43-46). *Revisit when:* SAT solver strategy is added to the registry and the solver can handle graph coloring search spaces.
- **Legendre's Conjecture** (prime between n² and (n+1)²). *Revisit when:* solver handles interval primality certification and can express Ingham-type estimates.

## Re-evaluation Hooks

1. **If the solver achieves `result: solved` on Erdős–Straus for all remaining hard residue classes** → reopen this research to select harder replacement problems from the Parked angles.
2. **If convergence tracking shows all three problems plateau at iteration 1-2 with zero progress** → the difficulty gradient is wrong; consider replacing Erdős–Straus with Hadamard 668 (search problem rather than proof problem) and Goldbach with R(5,5) (bounded numeric target).
