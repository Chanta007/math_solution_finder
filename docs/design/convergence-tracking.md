# Convergence Tracking

> Last updated: May 2026

## 1. Purpose

Defines how solver iterations are logged, how convergence is detected, and how different solution paths are tracked across runs. This is the primary mechanism for understanding what approaches were tried, which succeeded, which hit dead ends, and whether the solver is making progress.

## 2. Key Files

| File | Responsibility |
|------|---------------|
| `src/math_solver/engine/convergence.py` | Convergence detection and scoring |
| `src/math_solver/types/convergence.py` | ConvergenceEntry, Path, RunSummary types |
| `docs/convergence/` | Append-only JSONL logs (repo-tracked) |
| `docs/research/` | Research archives from each iteration |

## 3. JSONL Schema

Each line in a convergence log file is a JSON object:

```json
{
  "run_id": "run-2026-05-25-143022",
  "iteration": 5,
  "timestamp": "2026-05-25T14:35:12Z",
  "problem_hash": "sha256:abc123...",
  "strategy": "symbolic",
  "approach": "proof by contradiction via infinite descent",
  "result": "progress",
  "confidence": 0.72,
  "findings": "Established base case; inductive step needs field extension argument",
  "dead_ends": ["direct substitution", "generating function approach"],
  "tokens_used": 4523,
  "cost_usd": 0.045,
  "duration_s": 12.3,
  "parent_iteration": 4,
  "path_id": "path-symbolic-001"
}
```

### Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `run_id` | string | Unique run identifier (date + time) |
| `iteration` | int | Iteration number within this run |
| `timestamp` | ISO 8601 | When iteration completed |
| `problem_hash` | string | SHA-256 of problem description (for grouping) |
| `strategy` | string | Strategy used (symbolic, numeric, hybrid, etc.) |
| `approach` | string | Human-readable description of the approach |
| `result` | enum | `solved`, `progress`, `dead_end`, `error` |
| `confidence` | float | 0.0-1.0 confidence score from Claude |
| `findings` | string | Key findings from this iteration |
| `dead_ends` | string[] | Approaches confirmed as dead ends |
| `tokens_used` | int | Total Claude API tokens consumed |
| `cost_usd` | float | Estimated API cost for this iteration |
| `duration_s` | float | Wall-clock time in seconds |
| `parent_iteration` | int | Which prior iteration this builds on |
| `path_id` | string | Identifier for the solution path branch |

### Result Enum

| Value | Meaning | Next Action |
|-------|---------|-------------|
| `solved` | Problem solved — verified by sympy/numpy | Stop loop, output solution |
| `progress` | Partial progress — new insights gained | Continue loop |
| `dead_end` | Approach exhausted — no further progress possible | Try different strategy |
| `error` | API or computation error | Retry or surface |

## 4. Convergence Detection

Convergence is detected when:
1. **Solution found** — `result == "solved"` with verification passing
2. **Confidence plateau** — last N iterations show no improvement in confidence
3. **Path exhaustion** — all registered strategies have been tried with dead_end results
4. **Iteration limit** — `max_iterations` reached

The convergence score is computed from:
- Highest confidence across all iterations
- Rate of confidence change (slope over last 5 iterations)
- Number of unique strategies attempted
- Ratio of `progress` to `dead_end` results

## 5. Path Branching

When the solver detects that multiple promising approaches exist, it can branch:

```
Iteration 1 (analysis) → path-main
  ├── Iteration 2 (symbolic) → path-symbolic-001
  │     ├── Iteration 3 (refine) → path-symbolic-001
  │     └── Iteration 4 (dead_end) → path-symbolic-001 [CLOSED]
  └── Iteration 2b (numeric) → path-numeric-001
        └── Iteration 3 (progress) → path-numeric-001
```

Path branching integrates with `/mindcoachlabs:orchestrate` — parallel agents can explore different paths simultaneously across worktrees.

## 6. File Organization

```
docs/convergence/
├── run-2026-05-25-143022.jsonl     # One file per solver run
├── run-2026-05-25-160045.jsonl
└── summary.md                       # Auto-generated summary (optional)
```

Files are append-only and repo-tracked. Never edit or delete convergence logs — they are the audit trail for solver behavior.

## 7. Cross-references

- Core architecture: `docs/design/core-architecture.md`
- Observability: `docs/design/observability.md`
- Deferred approaches: `docs/deferred/index.md` (via `/mindcoachlabs:triage`)
