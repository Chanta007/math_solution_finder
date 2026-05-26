# Deployment

> Last updated: May 2026

## 1. Purpose

Defines installation, packaging, and optional Docker deployment for Math Solution Finder. The primary deployment mode is local CLI installation via pip/uv. Docker is available for reproducibility.

## 2. Key Files

| File | Responsibility |
|------|---------------|
| `pyproject.toml` | Package metadata, dependencies, entry points |
| `Dockerfile` | Optional containerized build |
| `.github/workflows/ci.yml` | CI pipeline (lint, type-check, test) |

## 3. Installation

### Local (recommended)

```bash
# Clone and install
git clone <repo-url>
cd math_solution_finder
pip install -e ".[dev]"
# or
uv pip install -e ".[dev]"

# Configure
cp .env.example .env
# Edit .env to add ANTHROPIC_API_KEY

# Run
python -m math_solver solve --problem "..."
```

### Docker (optional)

```bash
docker build -t math-solver .
docker run --env-file .env math-solver solve --problem "..."
```

## 4. CI/CD Pipeline

```
Push → Lint (ruff) → Type Check (mypy) → Test (pytest) → Build Check
```

- Runs on every push to `dev` and PR to `main`
- No deployment stage (CLI tool — users install locally)
- Failed checks block merge

## 5. Dependencies

Managed in `pyproject.toml`:

```toml
[project]
dependencies = [
    "anthropic>=0.40",
    "sympy>=1.13",
    "numpy>=2.0",
    "structlog>=24.0",
    "pydantic-settings>=2.0",
    "click>=8.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "hypothesis>=6.0",
    "pytest-mock>=3.0",
    "mypy>=1.10",
    "ruff>=0.5",
]
```

## 6. Cross-references

- Config / env vars: `docs/design/config.md`
- Core architecture: `docs/design/core-architecture.md`
