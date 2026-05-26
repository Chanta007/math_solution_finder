# Core Architecture

> Last updated: May 2026

## 1. Purpose

Defines the solver engine architecture for Math Solution Finder — a Python CLI tool that agentically searches for solutions to unsolved math problems through iterative solve loops, strategy selection, and convergence tracking.

## 2. Key Files

| File | Responsibility |
|------|---------------|
| `src/math_solver/engine/solver.py` | Main solver loop — orchestrates iterations |
| `src/math_solver/engine/convergence.py` | Convergence detection and path tracking |
| `src/math_solver/strategies/registry.py` | Strategy registration and selection |
| `src/math_solver/strategies/symbolic.py` | Sympy-based symbolic solving strategy |
| `src/math_solver/strategies/numeric.py` | Numpy-based numeric testing strategy |
| `src/math_solver/infrastructure/llm.py` | Claude API client factory |
| `pyproject.toml` | Dependencies, scripts, project metadata |

## 3. Technology Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| **Language** | Python 3.12+ (strict typing) | `mypy --strict` must pass |
| **CLI** | click or argparse | Commands in `math_solver/cli/` |
| **Math / Symbolic** | sympy | Symbolic computation and proof verification |
| **Math / Numeric** | numpy | Numeric testing and validation |
| **Primary LLM** | Anthropic Claude (`anthropic` SDK) | All calls via factory function |
| **Logging** | structlog | JSON to stderr |
| **Testing** | pytest + hypothesis | Property-based tests for math |
| **Config** | pydantic-settings | Central typed config from `.env` |
| **Deployment** | Docker (optional) | Local CLI is primary |

## 4. Project Structure

```
math_solution_finder/
├── src/
│   └── math_solver/
│       ├── __init__.py
│       ├── __main__.py              # python -m math_solver entrypoint
│       ├── cli/                     # CLI commands (solve, loop, report)
│       │   ├── __init__.py
│       │   ├── solve.py
│       │   ├── loop.py
│       │   └── report.py
│       ├── engine/                  # Solver engine
│       │   ├── __init__.py
│       │   ├── solver.py            # Main agentic loop
│       │   └── convergence.py       # Convergence detection
│       ├── strategies/              # Solving strategies (pluggable)
│       │   ├── __init__.py
│       │   ├── registry.py          # Strategy registry
│       │   ├── base.py              # Base strategy protocol
│       │   ├── symbolic.py          # Sympy-based
│       │   ├── numeric.py           # Numpy-based
│       │   └── hybrid.py            # Combined approaches
│       ├── math_core/               # Math primitives
│       │   ├── __init__.py
│       │   ├── expressions.py       # Expression manipulation
│       │   └── verification.py      # Result verification
│       ├── infrastructure/          # Cross-cutting concerns
│       │   ├── __init__.py
│       │   ├── llm.py               # Claude API client factory
│       │   ├── logging.py           # structlog configuration
│       │   └── config.py            # Central config (pydantic)
│       └── types/                   # Shared type definitions
│           ├── __init__.py
│           ├── problem.py           # Problem, Approach, Result types
│           └── convergence.py       # ConvergenceEntry, Path types
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── docs/                            # HARNESS documentation
│   ├── convergence/                 # Append-only solver path logs
│   └── research/                    # Research iteration archives
├── pyproject.toml
├── .env.example
└── launch_worktree.py
```

## 5. Solver Loop Flow

```
┌─────────────────────────────────────────────────────┐
│                    CLI Entrypoint                     │
│         (solve, loop, report commands)               │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                  Solver Engine                        │
│  ┌─────────┐  ┌────────────┐  ┌──────────────────┐  │
│  │ Problem  │  │  Strategy  │  │   Convergence    │  │
│  │ Analyzer │  │  Selector  │  │    Tracker       │  │
│  └────┬─────┘  └─────┬──────┘  └───────┬──────────┘  │
└───────┼──────────────┼──────────────────┼─────────────┘
        │              │                  │
┌───────▼──────────────▼──────────────────▼─────────────┐
│                   Strategies                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐ │
│  │ Symbolic  │  │ Numeric  │  │  Hybrid / Custom     │ │
│  │ (sympy)   │  │ (numpy)  │  │  (registered)        │ │
│  └──────────┘  └──────────┘  └──────────────────────┘ │
└───────────────────────┬───────────────────────────────┘
                        │
┌───────────────────────▼───────────────────────────────┐
│                 Infrastructure                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌───────┐ │
│  │ LLM      │  │ Logger   │  │ Config   │  │ File  │ │
│  │ Factory  │  │(structlog)│  │(pydantic)│  │  I/O  │ │
│  └──────────┘  └──────────┘  └──────────┘  └───────┘ │
└───────────────────────────────────────────────────────┘
```

### Single Iteration Flow

1. **Problem input** — CLI receives problem description (text or file path)
2. **Analysis** — Claude API analyzes the problem, identifies type and known approaches
3. **Strategy selection** — Based on analysis, select from registered strategies
4. **Approach generation** — Claude API generates a specific approach within the selected strategy
5. **Symbolic test** — Sympy verifies the approach symbolically (if applicable)
6. **Numeric test** — Numpy tests with concrete values
7. **Result evaluation** — Classify as: solved, progress, dead-end, or needs-more-iteration
8. **Convergence log** — Append iteration result to JSONL convergence log
9. **Loop decision** — If not solved and not converged, feed findings back to step 2

## 6. Configuration

See `docs/design/config.md` for environment variables and settings.

## 7. Cross-references

- CLI commands: `docs/design/command-reference.md`
- Convergence tracking: `docs/design/convergence-tracking.md`
- Observability: `docs/design/observability.md`
- Testing: `docs/design/testing.md`
- Deployment: `docs/design/deployment.md`
