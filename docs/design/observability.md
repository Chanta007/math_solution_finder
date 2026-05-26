# Observability

> Last updated: May 2026

## 1. Purpose

Defines the logging and metrics strategy for Math Solution Finder. As a CLI tool, observability is file-based: structured JSON logs on stderr, convergence tracking in append-only JSONL files, and Claude API usage metrics embedded in convergence entries.

## 2. Key Files

| File | Responsibility |
|------|---------------|
| `src/math_solver/infrastructure/logging.py` | structlog configuration and formatters |
| `src/math_solver/engine/convergence.py` | Convergence log writer (JSONL) |
| `docs/convergence/` | Append-only solver iteration logs |

## 3. Architecture

### Observability Stack

```
CLI Application
  ├─ Structured Logs → stderr (JSON via structlog)
  │     └─ Pipe to file: python -m math_solver loop ... 2> solver.log
  ├─ Convergence Logs → docs/convergence/*.jsonl (append-only, repo-tracked)
  └─ Claude API Metrics → embedded in convergence entries (tokens, cost, latency)
```

No APM, no Grafana, no external metrics stack. The tool runs locally; all observability is self-contained in log files.

## 4. Structured Logging

### Configuration

```python
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
)
```

### Log Entry Format

Every log entry includes:
- **timestamp** (ISO 8601)
- **level** (debug, info, warning, error)
- **component** (cli, engine, strategy, llm, config)
- **operation** (what function/step)
- **run_id** (correlates entries within a solver run)
- **iteration** (which solver iteration, if applicable)

### Example

```python
logger.info(
    "iteration_complete",
    component="engine",
    run_id="run-2026-05-25",
    iteration=5,
    strategy="symbolic",
    result="progress",
    confidence=0.72,
    duration_s=12.3,
)
```

## 5. Claude API Metrics

Tracked per iteration in convergence log entries:
- `tokens_used` — total input + output tokens
- `cost_usd` — estimated cost (computed from model pricing)
- `duration_s` — wall-clock time for the API call

Aggregate metrics (total tokens, total cost, average latency) are computed by the `report` command from convergence logs.

## 6. Error Handling

All catch blocks include structured logging. No silent catches.

```python
try:
    result = await llm_client.complete(prompt)
except anthropic.APIError as e:
    logger.error("llm_api_error", error=str(e), component="llm", operation="complete")
    raise
```

## 7. Cross-references

- Convergence log schema: `docs/design/convergence-tracking.md`
- Core architecture: `docs/design/core-architecture.md`
- **[CONSTRAINTS.md](../CONSTRAINTS.md)** — Observability rules (§5)
