## PR Metadata
- **Type**: feature
- **Research**: docs/research/2026-05-25-unsolved-math-test-cases.md
- **Research summary**: Erdős–Straus selected as easy-tier test case; proof-by-residue-cases approach
- **Evidence**: Wikipedia, arXiv, FrontierMath benchmarks
- **Commit**: feat: scaffold harness-as-solver + first proof-based Erdős–Straus iteration
- **Files changed**: scripts/erdos_straus.py, scripts/verify_proof.py, scripts/log_convergence.py, scripts/requirements.txt, tests/*, docs/orchestration-issues.md, docs/convergence/*, CLAUDE.md, docs/design/core-architecture.md
- **Design docs**: core-architecture.md, convergence-tracking.md, command-reference.md

# HARNESS Plan: Harness-as-Solver Scaffold + Proof-Based Erdős–Straus Iteration

| Field | Value |
|-------|-------|
| Type | feature |
| Status | build-complete |
| Short slug | harness-proof-solver |
| Created | 2026-05-26 |
| Branch | feature/feat1 |
| Design docs | core-architecture.md, convergence-tracking.md, command-reference.md, config.md |
| Prior plans | 2026-05-26-build-solver-engine.md (cancelled — API-based CLI overkill), harness-as-solver v1 (modified — pivoted from brute-force to proof-based) |

**Auto-loaded research**: docs/research/2026-05-25-unsolved-math-test-cases.md — Erdős–Straus as easy-tier first target (4/n = 1/x + 1/y + 1/z, polynomial form, residue reduction mod 840)

## Outcome Boundary

### Done when:
- A proof verification script can symbolically check algebraic identities for Erdős–Straus decompositions
- The first solver iteration uses Claude reasoning to analyze proof strategies (not brute-force), logs findings to `docs/convergence/`
- The convergence entry captures: which proof approach was attempted, what progress was made, what the next approach should be
- `pytest tests/` passes for all scripts including proof verification

### Failed when:
- The first iteration just runs brute-force search instead of attempting mathematical reasoning
- Convergence log entries don't describe proof strategies or mathematical insights
- Python scripts are used to SEARCH for solutions rather than VERIFY proof steps

### Must not:
- Require any API keys
- Use brute-force as the primary solving approach (only for verification/sanity-checking)
- Pollute main context with raw computation (use subagents)

## Steps

### 1. Create Erdős–Straus computation script — `done`
- **File(s):** `scripts/erdos_straus.py`, `scripts/requirements.txt`
- **Short slug:** erdos-straus-script
- **Action:** Standalone Python script (stdlib + sympy) with CLI interface:
  - `check N`: find x,y,z satisfying 4/N = 1/x + 1/y + 1/z
  - `range START END`: test all n in range, report statistics
  - `analyze N`: show residue class mod 840, applicable known results
  - Algorithm: greedy decomposition first, then systematic search
- **Acceptance:** `python scripts/erdos_straus.py check 5` outputs valid solution; `range 2 100` shows >95% solve rate

### 2. Create convergence log writer — `done`
- **File(s):** `scripts/log_convergence.py`
- **Short slug:** convergence-writer
- **Action:** Standalone Python script appending JSONL entries to `docs/convergence/`. Schema matches convergence-tracking.md.
- **Acceptance:** Creates valid JSONL files

### 3. Create orchestration issues tracker — `done`
- **File(s):** `docs/orchestration-issues.md`
- **Short slug:** orch-issues-tracker
- **Action:** Tracking doc for autonomy blockers with schema and categories.
- **Acceptance:** File exists with clear schema

### 4. Update CLAUDE.md with solver workflow — `done`
- **File(s):** `CLAUDE.md`
- **Short slug:** solver-workflow-docs
- **Action:** Added harness-as-solver workflow section.
- **Acceptance:** New sessions can follow the workflow

### 5. Update core-architecture.md for harness-as-solver pivot — `done`
- **File(s):** `docs/design/core-architecture.md`
- **Short slug:** arch-pivot
- **Action:** Replaced Python CLI architecture with harness-as-solver.
- **Acceptance:** Design doc reflects current architecture

### 6. Create proof verification script — `done`
- **File(s):** `scripts/verify_proof.py`
- **Short slug:** proof-verifier
- **Action:** Standalone Python script (stdlib + sympy) that verifies algebraic proof claims for Erdős–Straus. CLI interface:
  - `identity --expr "4*x*y*z == n*(x*y + x*z + y*z)" --subs "n=5,x=2,y=4,z=20"`: verify a specific substitution
  - `residue --n N`: verify which residue class mod 840 n belongs to and list known parametric solutions for that class
  - `parametric --formula "x=ceil(n/4), y=..., z=..."`: test if a parametric formula works for a range of n values
  Uses sympy.simplify, sympy.solve, and sympy.Rational for exact arithmetic. Returns JSON with verified/failed status and symbolic details.
- **Acceptance:** `python scripts/verify_proof.py identity --expr "4*x*y*z == n*(x*y + x*z + y*z)" --subs "n=5,x=2,y=4,z=20"` returns `{"verified": true}`

### 7. Execute proof-based first iteration on Erdős–Straus — `done`
- **File(s):** `docs/convergence/run-*.jsonl` (new)
- **Short slug:** proof-iteration-1
- **Action:** Execute the first proof-based solver iteration using Claude reasoning:
  1. **Analyze**: Claude reasons about the Erdős–Straus conjecture structure — identify the 6 hard residue classes mod 840, known parametric solutions, and open cases
  2. **Strategy**: Attempt proof by cases — for each residue class r mod 840, try to construct an explicit parametric solution x(n), y(n), z(n) that works for all n ≡ r (mod 840)
  3. **Verify**: Use `scripts/verify_proof.py` via subagent to check each parametric formula symbolically
  4. **Evaluate**: Record which residue classes have verified parametric solutions and which remain open
  5. **Log**: Run `scripts/log_convergence.py` with strategy="proof-by-residue-cases", recording which classes were solved and what the next approach should be
  6. **Track issues**: Log any orchestration issues to docs/orchestration-issues.md
- **Acceptance:** Convergence log has an entry describing proof strategies attempted, residue classes analyzed, and concrete next steps

### 8. Unit tests for all scripts — `done`
- **File(s):** `tests/test_erdos_straus.py`, `tests/test_log_convergence.py`, `tests/test_verify_proof.py`
- **Short slug:** script-tests
- **Action:** pytest tests:
  - test_erdos_straus: verify known solutions (n=5), reject invalid solutions, test range scan
  - test_log_convergence: verify JSONL schema compliance, file append behavior, required field validation
  - test_verify_proof: verify identity checking (valid and invalid substitutions), parametric formula testing, residue class analysis
- **Acceptance:** `pytest tests/ -v` all pass

## Deferred

### Phase 2: Collatz + Goldbach proof strategies
- Apply proof-based approach to the other two research problems
- *Revisit when:* Erdős–Straus proof iteration loop is working and has produced at least one verified parametric solution

### Phase 3: Automated loop scheduling
- Use `/loop` or `/schedule` to run solver iterations on a recurring basis
- *Revisit when:* manual harness-loop iterations demonstrate the workflow works end-to-end

### Phase 4: Cross-worktree convergence aggregation
- Merge convergence logs from parallel orchestrate runs into a unified view
- *Revisit when:* orchestrate has been used for at least 2 parallel solver runs
