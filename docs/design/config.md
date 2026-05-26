# Configuration

> Last updated: May 2026

## 1. Purpose

Documents all environment variables, configuration patterns, and the central config module for Math Solution Finder.

## 2. Key Files

| File | Responsibility |
|------|---------------|
| `src/math_solver/infrastructure/config.py` | Central config module (pydantic-settings) |
| `.env` | Local environment variables (gitignored) |
| `.env.example` | Template with placeholder values (committed) |

## 3. Environment Variables

### Required

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude solver calls |

### Optional

| Variable | Default | Description |
|----------|---------|-------------|
| `MATH_SOLVER_LOG_LEVEL` | `INFO` | Log level: DEBUG, INFO, WARNING, ERROR |
| `MATH_SOLVER_MAX_ITERATIONS` | `10` | Default max iterations for solver loops |
| `MATH_SOLVER_CONVERGENCE_DIR` | `docs/convergence` | Directory for convergence JSONL logs |
| `MATH_SOLVER_MODEL` | `claude-sonnet-4-5-20250514` | Claude model for solver calls |
| `MATH_SOLVER_MAX_TOKENS` | `4096` | Max tokens per Claude API call |
| `MATH_SOLVER_TEMPERATURE` | `0.7` | Temperature for approach generation |

## 4. Central Config Module

```python
# src/math_solver/infrastructure/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    anthropic_api_key: str
    log_level: str = "INFO"
    max_iterations: int = 10
    convergence_dir: str = "docs/convergence"
    model: str = "claude-sonnet-4-5-20250514"
    max_tokens: int = 4096
    temperature: float = 0.7

    class Config:
        env_prefix = "MATH_SOLVER_"
        env_file = ".env"

settings = Settings()
```

**Rules**:
- All env var reads go through this module. No scattered `os.environ` reads.
- Validated at startup — fails fast with clear error if `ANTHROPIC_API_KEY` is missing.
- The `ANTHROPIC_API_KEY` has no `MATH_SOLVER_` prefix (standard naming).

## 5. Cross-references

- Core architecture: `docs/design/core-architecture.md`
- Deployment: `docs/design/deployment.md`
