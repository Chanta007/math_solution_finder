# Command Reference

> Last updated: May 2026

## 1. Purpose

Documents all CLI commands, their flags, and usage patterns for the Math Solution Finder tool.

## 2. Key Files

| File | Responsibility |
|------|---------------|
| `src/math_solver/__main__.py` | `python -m math_solver` entrypoint |
| `src/math_solver/cli/solve.py` | Single-shot solve command |
| `src/math_solver/cli/loop.py` | Agentic loop command |
| `src/math_solver/cli/report.py` | Convergence report generation |

## 3. Commands

### `solve` — Single-shot problem solving

```bash
python -m math_solver solve --problem "Prove that sqrt(2) is irrational"
python -m math_solver solve --file problem.md
python -m math_solver solve --problem "..." --strategy symbolic
```

| Flag | Default | Description |
|------|---------|-------------|
| `--problem` | (required) | Problem description text |
| `--file` | — | Read problem from file (mutually exclusive with --problem) |
| `--strategy` | auto | Strategy: auto, symbolic, numeric, hybrid |
| `--output` | stdout | Output file path (JSON) |
| `-v` / `--verbose` | false | Increase log verbosity |

### `loop` — Agentic solver loop

```bash
python -m math_solver loop --problem "..." --max-iterations 20
python -m math_solver loop --file problem.md --convergence-threshold 0.95
```

| Flag | Default | Description |
|------|---------|-------------|
| `--problem` | (required) | Problem description text |
| `--file` | — | Read problem from file |
| `--max-iterations` | 10 | Maximum solver iterations |
| `--convergence-threshold` | 0.9 | Stop when convergence score exceeds this |
| `--log-dir` | docs/convergence/ | Where to write convergence logs |
| `--resume` | — | Resume from a previous convergence log file |
| `-v` / `--verbose` | false | Increase log verbosity |

### `report` — Convergence analysis

```bash
python -m math_solver report --log docs/convergence/run-2026-05-25.jsonl
python -m math_solver report --log docs/convergence/ --format markdown
```

| Flag | Default | Description |
|------|---------|-------------|
| `--log` | (required) | Path to convergence log file or directory |
| `--format` | text | Output format: text, json, markdown |
| `--summary-only` | false | Show only summary, not per-iteration details |

## 4. Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (solution found or report generated) |
| 1 | Error (API failure, invalid input, solver error) |
| 2 | Usage error (invalid flags, missing required args) |
| 3 | No solution found within iteration limit |

## 5. Cross-references

- Core architecture: `docs/design/core-architecture.md`
- Config / env vars: `docs/design/config.md`
