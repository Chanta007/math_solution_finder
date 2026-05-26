# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> **This is a condensed quick reference.** Full architectural rules: `docs/CONSTRAINTS.md`. Documentation governance and templates: `docs/HARNESS.md`.

## Quick Start Commands

```bash
# Run solver
python -m math_solver solve --problem "problem description"

# Run solver loop (agentic)
python -m math_solver loop --problem "problem description" --max-iterations 10

# Test
pytest

# Lint
ruff check .

# Type check
mypy src/

# Format
ruff format .
```

**Before Committing**:
1. Run tests: `pytest`
2. Run type checker: `mypy src/`
3. Run linter: `ruff check .`
4. Update relevant `docs/design/*.md` if architecture/data models/flows changed

**Git Workflow**: Work on feature branches. PRs target `dev`. For parallel work: `python launch_worktree.py {name}` (creates worktree, copies `.env` files).

## Architecture Overview

Math Solution Finder uses **Claude Code + MindCoachLabs harness** as the agentic solver — no external API keys needed. Claude Code IS the reasoning engine; Python scripts handle computation.

### Solver Workflow (Harness-as-Solver)

Each solver iteration is a harness cycle:

1. **Research** — `/mindcoachlabs:research <approach>` analyzes the problem, identifies strategies
2. **Plan + Build** — `/mindcoachlabs:plan auto` writes a Python computation script, runs it via subagent, evaluates results
3. **Log convergence** — `python scripts/log_convergence.py` appends JSONL to `docs/convergence/`
4. **Triage dead ends** — `/mindcoachlabs:triage` reviews deferred approaches in `docs/deferred/index.md`
5. **Repeat** — findings feed into the next `/mindcoachlabs:research` iteration

**Key principles:**
- **Subagents for computation**: Use the `Agent` tool to run Python scripts, keeping the main context window clean for reasoning and strategy
- **Parallel exploration**: `/mindcoachlabs:orchestrate` fans out approaches across worktrees
- **Convergence tracking**: Append-only JSONL in `docs/convergence/` (see `docs/design/convergence-tracking.md`)
- **Orchestration issue tracking**: Log autonomy blockers to `docs/orchestration-issues.md`
- **No API key needed**: Claude Code provides the intelligence; `scripts/` provides computation

### Computation Scripts

| Script | Purpose |
|--------|---------|
| `scripts/erdos_straus.py` | Find x,y,z satisfying 4/n = 1/x + 1/y + 1/z |
| `scripts/log_convergence.py` | Append JSONL convergence entry |

Run scripts via subagent to preserve main context:
```
Agent({ prompt: "Run python3 scripts/erdos_straus.py range 2 1000 and summarize" })
```

Parallel solver agents can be dispatched via `/mindcoachlabs:orchestrate`. Deferred approaches and dead-end paths are tracked via `/mindcoachlabs:triage` + `docs/deferred/index.md`.

### Documentation

| Doc | Purpose |
|-----|---------|
| `docs/CONSTRAINTS.md` | Architectural rules (the single source of truth) |
| `docs/design/*.md` | Domain-specific design specs |
| `docs/plans/*.md` | Step-by-step execution plans for common tasks |
| `docs/runbooks/*.md` | Debugging playbooks for known failure patterns |
| `docs/HARNESS.md` | Documentation governance, templates, full doc index |
| `docs/convergence/` | Append-only convergence logs tracking solver paths |
| `docs/research/` | Research archives from each solver iteration |

**Reading order for a task**: CLAUDE.md (auto-loaded) → Source-to-doc mapping below → relevant `design/*.md` → `CONSTRAINTS.md` section → `plans/*.md` if applicable.

### Task Navigation

| I want to... | Read |
|--------------|------|
| Add a new solver strategy | `plans/add-feature.md` then `design/core-architecture.md` |
| Add test coverage | `plans/add-test.md` then `design/testing.md` |
| Add a new CLI command | `design/command-reference.md` |
| Add observability | `plans/add-observability.md` then `design/observability.md` |
| Understand convergence tracking | `design/convergence-tracking.md` |
| Debug solver failures | `design/observability.md` then `runbooks/` |
| Work on parallel features | use `python launch_worktree.py` |
| Start any task (gateway routes to right skill) | `/mindcoachlabs:mcl <describe what you want>` |
| Research options before planning a non-trivial choice | `/mindcoachlabs:mcl research <topic>` |
| Use MindCoachLabs workflow (plan/build/verify) | `/mindcoachlabs:plan` → `/mindcoachlabs:build` → `/mindcoachlabs:verify` |
| Modify an active plan mid-build | `/mindcoachlabs:plan modify: <what to change>` |
| Diagnose harness issues | `/mindcoachlabs:health-check` or `/mindcoachlabs:health-check --fix` |
| Run parallel solver agents | `/mindcoachlabs:orchestrate` |
| Review deferred approaches | `/mindcoachlabs:triage` |

### Source File to Design Doc Mapping

- CLI entry points / commands → `docs/design/command-reference.md`
- Solver engine / loop logic → `docs/design/core-architecture.md`
- Convergence tracking → `docs/design/convergence-tracking.md`
- Configuration / env vars → `docs/design/config.md`
- Tests → `docs/design/testing.md`
- Logging / metrics → `docs/design/observability.md`
- Deployment / Docker → `docs/design/deployment.md`

### Dependency Layers (strict downward flow)

```
CLI ENTRYPOINTS  → Entry points (solve, loop, report commands)
SOLVER ENGINE    → Agentic loop orchestration, convergence tracking
STRATEGIES       → Problem-specific solving approaches (symbolic, numeric, hybrid)
MATH CORE        → Symbolic computation (sympy), numeric testing (numpy), proof verification
INFRASTRUCTURE   → LLM client factory, logging, config, file I/O
```

Rules: Higher layers may import lower layers. Never the reverse. CLI entrypoints never import from math core directly (go through solver engine).

### Core Architecture Patterns

**Factory Pattern**: All external service connections (Claude API, future LLM providers) go through factory functions. Never instantiate SDK clients directly. Factories handle configuration, credential resolution, rate limiting, and usage tracking.

**Strategy Registry**: Solver strategies (symbolic, numeric, hybrid, proof-by-contradiction, etc.) register via a registry. The solver engine never checks for specific strategy types — it iterates registered strategies.

**Central Config**: One module (`math_solver/config.py`) reads all env vars and exports typed configuration. No scattered `os.environ` reads.

**Convergence Logger**: Append-only JSONL writer that records every solver iteration's approach, result, and path metadata to `docs/convergence/`.

### Observability

No bare `print()` in production code. Use structured logging:
- `structlog` for JSON-formatted stderr output
- Correlation IDs for tracing solver iterations
- Metrics for Claude API calls (latency, token usage, cost)
- Convergence logs for tracking solver paths

### Key Technologies

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12+ (strict typing with mypy) |
| CLI Framework | click or argparse |
| Math / Symbolic | sympy, numpy |
| AI / LLM | anthropic SDK (Claude API) |
| Logging | structlog (JSON to stderr) |
| Testing | pytest + hypothesis (property-based) |
| Linting | ruff |
| Type Checking | mypy (strict mode) |
| Package Manager | uv / pip with pyproject.toml |
| Deployment | Docker (optional), local CLI primary |

## Environment Setup

**Secrets management**: API keys in `.env` (gitignored). Never commit plaintext secrets.

Required environment variables:
```bash
ANTHROPIC_API_KEY=<your-key-here>    # Required for solver loops
```

Optional:
```bash
MATH_SOLVER_LOG_LEVEL=INFO           # DEBUG, INFO, WARNING, ERROR
MATH_SOLVER_MAX_ITERATIONS=10        # Default max iterations per solve loop
MATH_SOLVER_CONVERGENCE_DIR=docs/convergence  # Where to write convergence logs
```

Environment detection is centralized in `math_solver/config.py`. Never hardcode environment checks.

## Important Conventions

### Pre-Commit Checklist
1. Tests pass: `pytest`
2. Type checker clean: `mypy src/`
3. Linter clean: `ruff check .`
4. Convergence logs committed if solver was run

### Security
- All API keys managed via `.env` (gitignored)
- No secrets in convergence logs or research archives
- Claude API calls use rate limiting with exponential backoff
