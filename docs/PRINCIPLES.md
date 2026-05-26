# Project Principles

> Extracted from `HARNESS.md` §1 and `CONSTRAINTS.md` "Why" / "Rationale" sections.
> These are the stable "why" statements that drive the "what" in design docs and the "how" in constraints. When a principle and a specific rule disagree, prefer the rule (the rule is the canonical *how*); update the principle in the next harness-review pass.
>
> Tailored for Math Solution Finder — a Python CLI tool for agentic math problem solving.

---

## Future-Proofing

**P1. Swappable over hard-coded**
All external service connections go through factory or registry patterns. This centralizes configuration, enables testing with mocks, provides observability hooks, and allows provider swaps — including LLM providers — without changing business logic.
> Source: CONSTRAINTS.md §2 Factory Pattern, §2 Plugin Registry

**P2. Stateless over sticky**
Architecture decisions favor horizontal scalability and operational simplicity. Prefer stateless services. Design for the 10x growth scenario without over-engineering for the 100x scenario.
> Source: HARNESS.md §1 "Scalable & Supportable"

---

## Single Source of Truth

**P3. One design doc per domain**
Each architectural domain has exactly one design doc. No duplication across files. Constraints are declarative in `CONSTRAINTS.md`, not scattered across design docs.
> Source: HARNESS.md §2.1 Principles 1–2

**P4. Central configuration**
All environment variables are read in one place and exported as typed configuration. No scattered `process.env` / `os.environ` reads. Secrets are managed per-environment.
> Source: CONSTRAINTS.md §11.1, §6.4

**P5. One commit, one complete story**
Code + docs + types + tests + observability must all be consistent in a single commit. No partial commits. No orphaned TODOs left in committed code.
> Source: HARNESS.md §2.4 rule 6, §2.1 Principle 6

---

## Evolution Readiness

**P6. Visibility through versioning**
Distribution channels must surface change to users. Silent updates erode trust faster than explicit breakage; semver bumps are how the harness signals "I changed" to users who pull updates.
> Source: CONSTRAINTS.md §15.9

**P7. Diagnostics mirror reality**
Stale checks erode trust faster than missing checks. Health diagnostics must keep pace with what the system actually does, or users learn to ignore them.
> Source: CONSTRAINTS.md §15.10

**P8. Stability through indirection**
User-facing identifiers survive backend churn by pointing through stable aliases. Versioned cache paths break on update; a `current/` symlink decouples the user-visible identifier from the moving target underneath.
> Source: CONSTRAINTS.md §15.11

---

## Documentation Thrift

**P9. Delete, don't strike through**
Stale content is deleted. Historical specs move to `docs/archive/` with a date prefix. Stale docs that contradict the code are fixed — not left as warnings.
> Source: HARNESS.md §2.1 Principle 5, §2.5 Maintenance Rules

**P10. Leave it cleaner than found**
Every file touched is left cleaner than found. Proactive cleanup is a duty, not an optional polish pass.
> Source: HARNESS.md §2.1 Principle 7

**P11. Simplification bias**
Every change should reduce system complexity, not add to it. When in doubt, remove.
> Source: HARNESS.md §2.1 Principle 8

---

## Operational Resilience

Tooling: Python 3.12+ with `mypy --strict`, `ruff` for linting/formatting, `pydantic-settings` for config validation.

**P12. Static types over runtime checks**
Invalid states should be unrepresentable in the type system, not caught by tests at runtime. Types are executable documentation that never drift from the implementation. Tooling is chosen per-project based on language and industry standards (e.g., TypeScript strict mode, mypy, pyright, golangci-lint); the harness recommends the strictest available option.
> Source: HARNESS.md §2.4 rule 2 (build/typecheck), CONSTRAINTS.md §1 (typed exports), CONSTRAINTS.md §8.4 (pre-commit type check)

**P13. Fail fast at boundaries, recover gracefully in flow**
Invalid input is rejected immediately with a clear, actionable error. Programmer errors (null derefs, type mismatches) crash loudly in development. User-facing operations degrade gracefully — never expose internal stack traces or implementation details.
> Source: HARNESS.md §8.3 (input validation), CONSTRAINTS.md §6.3 (input security), CONSTRAINTS.md §5.4 (no silent catches)

**P14. API key protection**
The ANTHROPIC_API_KEY is the only secret. It is loaded from `.env` (gitignored), never logged, never written to convergence logs or research archives.
> Source: CONSTRAINTS.md §6.4 (secret management)

---

## Code Quality

**P15. Code is written for the next reader**
Simple over clever. Explicit over implicit. Small functions. Obvious naming. No dead code. Math code especially benefits from clear variable names — prefer `discriminant` over `d`.
> Source: HARNESS.md §1 "Clean, Clear Code"

---

## Product Quality

**P16. Observable via logs**
Every solver iteration is logged with structured context (structlog JSON on stderr). Every approach path is recorded in convergence logs. The `report` command provides post-hoc analysis without needing to re-run.
> Source: CONSTRAINTS.md §5

**P17. Convergence is the metric**
The solver's goal is convergence toward a solution. Every iteration must advance understanding — either by finding progress or eliminating a dead end. Both outcomes are valuable and tracked.
> Source: docs/design/convergence-tracking.md

**P18. Reproducibility**
Convergence logs are repo-tracked so any solver run can be analyzed, compared, or resumed. Research archives capture the reasoning at each step.
> Source: docs/design/convergence-tracking.md §6

---

## Self-Improvement

**P20. Propose, don't apply**
Harness mutations require user confirmation per change. Skills like `/mindcoachlabs:harness-review` and `/mindcoachlabs:do` never auto-apply work that touches constraints, design docs, or principles. The cost of a missed proposal is low; the cost of an unintended automatic edit is high.
> Source: `plugins/mindcoachlabs/skills/harness-review/SKILL.md` deep-mode guardrails block, CONSTRAINTS.md §15.5 (do-skill scope)

**P21. Evidence beats opinion**
Pruning decisions cite per-model run counts, not assumptions. Conservative thresholds (≥20 records, segmented by `model_id`) protect against single-model overfitting; multi-model evidence is preferred before retiring a rule.
> Source: `plugins/mindcoachlabs/skills/harness-review/SKILL.md` deep-mode prerequisites
