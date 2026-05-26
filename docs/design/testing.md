# Testing

> Last updated: May 2026

## 1. Purpose

Automated testing ensures solver strategies produce correct results, the agentic loop behaves correctly under edge cases, and math operations are verified both symbolically and numerically. The strategy emphasizes property-based testing for mathematical correctness.

## 2. Key Files

| File | Responsibility |
|------|---------------|
| `pyproject.toml` | pytest + hypothesis configuration |
| `tests/conftest.py` | Shared fixtures (mock LLM client, sample problems) |
| `tests/unit/` | Unit tests for math core, strategies, config |
| `tests/integration/` | Integration tests for solver engine with mocked LLM |

## 3. Architecture

### Testing Pyramid

```
       / Integration  \        ~30% — Solver loop with mocked LLM
      /────────────────\
     /   Unit Tests     \      ~50% — Math operations, strategies, config
    /────────────────────\
   / Property-Based Tests \    ~20% — Hypothesis for math correctness
  /________________________\
```

### Framework Choices

| Tool | Layer | Why |
|------|-------|-----|
| pytest | Unit + Integration | Standard Python test runner, rich plugin ecosystem |
| hypothesis | Property-based | Generates random math inputs to find edge cases |
| pytest-mock | Mocking | Mock Claude API calls in integration tests |

## 4. Running Tests

```bash
# All tests
pytest

# Watch mode
pytest --watch

# Coverage
pytest --cov=math_solver

# Property-based only
pytest -m property

# Unit only
pytest tests/unit/

# Verbose
pytest -v
```

## 5. Test File Placement

Tests mirror the source structure:

```
tests/
├── conftest.py
├── unit/
│   ├── test_convergence.py
│   ├── test_registry.py
│   ├── test_symbolic.py
│   ├── test_numeric.py
│   └── test_config.py
├── integration/
│   ├── test_solver_loop.py
│   └── test_cli.py
└── properties/
    ├── test_math_properties.py
    └── test_convergence_properties.py
```

## 6. What to Test vs. Skip

| Test | Skip |
|------|------|
| Math operations (sympy expressions, numpy calculations) | Claude API response content (mock it) |
| Strategy selection logic | Convergence log file I/O (trust filesystem) |
| Convergence detection algorithm | CLI argument parsing (click/argparse handles it) |
| Config validation (missing keys, invalid values) | Exact LLM prompt wording |

## 7. Writing Tests

### Unit Test Pattern (Math)

```python
def test_symbolic_strategy_verifies_sqrt2_irrational():
    strategy = SymbolicStrategy()
    result = strategy.verify(
        claim="sqrt(2) is irrational",
        proof_steps=["assume p/q in lowest terms", "..."]
    )
    assert result.verified is True
```

### Property-Based Test Pattern

```python
from hypothesis import given, strategies as st

@given(st.integers(min_value=2, max_value=1000))
def test_prime_factorization_roundtrip(n):
    factors = factorize(n)
    assert product(factors) == n
    assert all(is_prime(f) for f in factors)
```

### Integration Test Pattern (Mocked LLM)

```python
def test_solver_loop_stops_on_solution(mock_llm):
    mock_llm.complete.side_effect = [
        AnalysisResponse(strategy="symbolic"),
        ApproachResponse(approach="direct proof"),
        EvaluationResponse(result="solved", confidence=0.99),
    ]
    result = run_solver_loop(problem="...", max_iterations=10)
    assert result.status == "solved"
    assert result.iterations == 1
```

## 8. Pre-Commit Checklist

All must pass before committing:
1. `pytest` — All tests pass
2. `mypy src/` — Type checker clean
3. `ruff check .` — Linter clean

## 9. Cross-references

- **[CONSTRAINTS.md](../CONSTRAINTS.md)** — Testing conventions (§8)
- **[HARNESS.md](../HARNESS.md)** — Code change workflow requiring tests (§2.4)
- **[plans/add-test.md](../plans/add-test.md)** — Step-by-step plan for adding tests
