# HARNESS Plan: Build Solver Engine for 3 Research Problems

| Field | Value |
|-------|-------|
| Type | feature |
| Status | approved |
| Short slug | build-solver-engine |
| Created | 2026-05-25 |
| Branch | feature/feat1 |
| Design docs | core-architecture.md, command-reference.md, convergence-tracking.md, config.md, testing.md, observability.md, deployment.md |
| Prior plans | 2026-05-25-bootstrap.md (harness setup, no implementation lessons) |

**Auto-loaded research**: docs/research/2026-05-25-unsolved-math-test-cases.md — Erdős–Straus + Collatz + Goldbach selected as solver test suite with difficulty gradient (easy/medium/hard)

## Outcome Boundary

### Done when:
- `python -m math_solver solve --problem "Find x,y,z such that 4/5 = 1/x + 1/y + 1/z"` produces a valid solution and exits 0
- `python -m math_solver loop --problem "..." --max-iterations 3` runs 3 iterations, writes JSONL to `docs/convergence/`, and each entry matches the convergence-tracking.md schema
- `pytest` passes with unit tests for all 3 problem formulations and integration tests with mocked LLM
- `mypy src/` passes with zero errors (strict mode)
- `ruff check .` passes clean

### Failed when:
- Solver crashes on any of the 3 research problems instead of gracefully logging the error
- Convergence log entries are missing required fields (run_id, iteration, strategy, result, confidence)
- LLM client is instantiated directly instead of through the factory
- `os.environ` reads appear outside `config.py`

### Must not:
- Log or print the ANTHROPIC_API_KEY
- Import upward in the dependency layer hierarchy (e.g., infrastructure importing from engine)
- Use bare `print()` anywhere — structlog only

## Steps

### 1. Project scaffolding — `pending`
- **File(s):** `pyproject.toml`, `src/math_solver/__init__.py`, `src/math_solver/__main__.py`
- **Short slug:** project-scaffold
- **Action:** Create pyproject.toml with project metadata, dependencies (anthropic>=0.40, sympy>=1.13, numpy>=2.0, structlog>=24.0, pydantic-settings>=2.0, click>=8.0) and dev deps (pytest>=8.0, hypothesis>=6.0, pytest-mock>=3.0, mypy>=1.10, ruff>=0.5). Create src/math_solver/__init__.py (version string) and __main__.py (entry point calling CLI group).
- **Acceptance:** `pip install -e ".[dev]"` succeeds; `python -m math_solver` runs without import errors

### 2. Type definitions — `pending`
- **File(s):** `src/math_solver/types/__init__.py`, `src/math_solver/types/problem.py`, `src/math_solver/types/convergence.py`
- **Short slug:** type-defs
- **Action:** Define dataclasses/Pydantic models: Problem (description, category, formulation, verify_fn), Approach (strategy_name, description, steps), Result (status: solved|progress|dead_end|error, confidence: float, findings: str, dead_ends: list[str]), ConvergenceEntry (full JSONL schema: run_id, iteration, timestamp, problem_hash, strategy, approach, result, confidence, findings, dead_ends, tokens_used, cost_usd, duration_s, parent_iteration, path_id).
- **Acceptance:** mypy passes on types module; all fields match convergence-tracking.md schema

### 3. Infrastructure layer — `pending`
- **File(s):** `src/math_solver/infrastructure/__init__.py`, `src/math_solver/infrastructure/config.py`, `src/math_solver/infrastructure/logging.py`, `src/math_solver/infrastructure/llm.py`
- **Short slug:** infra-layer
- **Action:** config.py: pydantic Settings class with ANTHROPIC_API_KEY (no prefix), MATH_SOLVER_* env vars for log_level, max_iterations, convergence_dir, model, max_tokens, temperature. logging.py: structlog JSON config outputting to stderr with timestamper, log level, JSON renderer. llm.py: create_llm_client() factory wrapping anthropic.Anthropic, with retry logic (exponential backoff on 429/529, max 3 retries).
- **Acceptance:** Config validates at import (fails fast on missing API key), structlog outputs JSON to stderr, LLM factory returns anthropic.Anthropic client

### 4. Strategy registry + base protocol — `pending`
- **File(s):** `src/math_solver/strategies/__init__.py`, `src/math_solver/strategies/registry.py`, `src/math_solver/strategies/base.py`
- **Short slug:** strategy-registry
- **Action:** base.py: Strategy Protocol with methods analyze(problem) -> Approach and execute(problem, approach) -> Result. registry.py: StrategyRegistry class with register(name, strategy), get(name) -> Strategy, list_strategies() -> list[str]. Global registry instance. Never check for specific strategy types.
- **Acceptance:** Registry register/get/list works; mypy validates Protocol conformance

### 5. Symbolic strategy (sympy) — `pending`
- **File(s):** `src/math_solver/strategies/symbolic.py`
- **Short slug:** symbolic-strategy
- **Action:** SymbolicStrategy implementing Protocol. analyze(): returns approach based on problem category. execute(): dispatches to problem-specific symbolic verification — Erdős–Straus: solve 4*x*y*z = n*(x*y + x*z + y*z) using sympy.diophantine or systematic search; Collatz: symbolic orbit analysis with sympy; Goldbach: symbolic prime testing with sympy.isprime. Returns Result with confidence score.
- **Acceptance:** verify_erdos_straus(5) finds valid x,y,z; verify_collatz_orbit(27) returns orbit length

### 6. Numeric strategy (numpy) — `pending`
- **File(s):** `src/math_solver/strategies/numeric.py`
- **Short slug:** numeric-strategy
- **Action:** NumericStrategy implementing Protocol. execute(): Erdős–Straus: brute-force search for x,y,z up to configurable bound; Collatz: iterate and track orbit statistics (max value, length, convergence); Goldbach: test even numbers for prime pair sums using numpy sieve. Returns Result.
- **Acceptance:** Numeric search finds Erdős–Straus solution for n=5; Collatz orbit for n=27 converges

### 7. Problem definitions — `pending`
- **File(s):** `src/math_solver/problems/__init__.py`, `src/math_solver/problems/erdos_straus.py`, `src/math_solver/problems/collatz.py`, `src/math_solver/problems/goldbach.py`
- **Short slug:** problem-defs
- **Action:** Each file defines: PROBLEM constant (Problem instance with description, formulation, known bounds from research), verify(result) function that checks mathematical validity. erdos_straus: verify 4/n = 1/x + 1/y + 1/z holds. collatz: verify orbit reaches 1. goldbach: verify n = p + q with both prime.
- **Acceptance:** Each verify() correctly validates known results and rejects invalid ones

### 8. Convergence tracking — `pending`
- **File(s):** `src/math_solver/engine/__init__.py`, `src/math_solver/engine/convergence.py`
- **Short slug:** convergence-tracker
- **Action:** ConvergenceTracker class: __init__(run_id, log_dir), log_iteration(entry: ConvergenceEntry) appends JSON line to file, detect_convergence(entries) checks 4 conditions (solution found, confidence plateau over last 5, all strategies exhausted, iteration limit), get_summary() returns aggregate stats. File path: {log_dir}/run-{run_id}.jsonl.
- **Acceptance:** Creates valid JSONL files; detect_convergence triggers on each condition

### 9. Solver engine — `pending`
- **File(s):** `src/math_solver/engine/solver.py`
- **Short slug:** solver-engine
- **Action:** Solver class: __init__(llm_client, strategy_registry, convergence_tracker, config). run_single(problem) — one-shot solve. run_loop(problem, max_iterations) — agentic loop: analyze via LLM → select strategy → generate approach via LLM → execute strategy → evaluate → log convergence → decide continue/stop. Graceful SIGINT handler saves convergence state before exit. All LLM calls go through the factory client.
- **Acceptance:** run_loop with mocked LLM completes N iterations, writes convergence log, stops on solution or limit

### 10. CLI entrypoints — `pending`
- **File(s):** `src/math_solver/cli/__init__.py`, `src/math_solver/cli/solve.py`, `src/math_solver/cli/loop.py`, `src/math_solver/cli/report.py`
- **Short slug:** cli-commands
- **Action:** Click CLI group with 3 commands per command-reference.md: solve (--problem/--file, --strategy, --output, -v), loop (--problem/--file, --max-iterations, --convergence-threshold, --log-dir, --resume, -v), report (--log, --format text|json|markdown, --summary-only). Wire __main__.py to invoke CLI group. Exit codes: 0 success, 1 error, 2 usage, 3 no solution.
- **Acceptance:** `python -m math_solver --help` shows all 3 commands with correct flags

### 11. Unit tests — `pending`
- **File(s):** `tests/conftest.py`, `tests/unit/test_config.py`, `tests/unit/test_registry.py`, `tests/unit/test_symbolic.py`, `tests/unit/test_numeric.py`, `tests/unit/test_convergence.py`, `tests/unit/test_problems.py`
- **Short slug:** unit-tests
- **Action:** conftest.py: fixtures for mock LLM client, sample Problem instances for all 3 problems. Tests: config validation (missing key raises), registry (register/get/list/unknown raises), symbolic (Erdős–Straus n=5 solution, Collatz orbit n=27), numeric (brute-force Erdős–Straus, Collatz convergence), convergence (plateau detection, solution detection, file writing), problem verify functions (valid/invalid inputs).
- **Acceptance:** `pytest tests/unit/ -v` all pass

### 12. Integration tests — `pending`
- **File(s):** `tests/integration/test_solver_loop.py`, `tests/integration/test_cli.py`
- **Short slug:** integration-tests
- **Action:** test_solver_loop: mock LLM to return canned analysis + approach responses, verify run_loop executes correct number of iterations, writes convergence log with valid entries, stops on "solved" result. test_cli: use click.testing.CliRunner to invoke solve/loop/report commands, verify exit codes, output format, and error handling.
- **Acceptance:** `pytest tests/integration/ -v` all pass

## Deferred

### Phase 2: Hybrid strategy
- Combine symbolic + numeric for cross-validation
- *Revisit when:* basic symbolic and numeric strategies are working and tested

### Phase 3: LLM prompt engineering
- Optimize Claude prompts for each problem type (currently uses generic prompts)
- *Revisit when:* first solver runs show prompt quality is the bottleneck

### Phase 4: Resume from convergence log
- `--resume` flag to continue a previous solver run from its last iteration
- *Revisit when:* solver runs long enough that interruption is common
