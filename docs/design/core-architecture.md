# Core Architecture

> Last updated: May 2026

## 1. Purpose

Defines the harness-as-solver architecture for Math Solution Finder. Claude Code + MindCoachLabs harness commands serve as the agentic reasoning engine. Python scripts provide standalone computation (sympy/numpy). No external API keys required.

## 2. Key Files

| File | Responsibility |
|------|---------------|
| `scripts/erdos_straus.py` | Erdős–Straus conjecture computation (find x,y,z for 4/n = 1/x + 1/y + 1/z) |
| `scripts/log_convergence.py` | Append JSONL convergence entry to docs/convergence/ |
| `docs/convergence/` | Append-only solver iteration logs (JSONL) |
| `docs/research/` | Research archives from each solver iteration |
| `docs/deferred/index.md` | Parked approaches tracked via /mindcoachlabs:triage |
| `docs/orchestration-issues.md` | Autonomy blocker tracking |
| `CLAUDE.md` | Solver workflow documentation (auto-loaded by Claude Code) |

## 3. Technology Stack

| Layer | Technology | Notes |
|-------|-----------|-------|
| **Reasoning engine** | Claude Code (Opus) | MindCoachLabs harness provides workflow orchestration |
| **Computation** | Python 3.12+ scripts | Standalone, stdlib + sympy |
| **Math / Symbolic** | sympy | Used in computation scripts |
| **Workflow** | MindCoachLabs harness | research → plan auto → build → verify → triage |
| **Parallel** | /mindcoachlabs:orchestrate | Fan out approaches across worktrees |
| **Tracking** | JSONL convergence logs | Append-only, repo-tracked |
| **Testing** | pytest | Tests for computation scripts |

## 4. Project Structure

```
math_solution_finder/
├── scripts/                         # Standalone computation scripts
│   ├── erdos_straus.py              # Erdős–Straus solver
│   ├── log_convergence.py           # Convergence log writer
│   └── requirements.txt            # Script dependencies (sympy)
├── tests/                           # Tests for scripts
│   ├── test_erdos_straus.py
│   └── test_log_convergence.py
├── docs/
│   ├── convergence/                 # Append-only solver iteration logs
│   ├── research/                    # Research archives per iteration
│   ├── deferred/                    # Parked approaches
│   ├── orchestration-issues.md      # Autonomy blocker tracking
│   ├── design/                      # Architecture specs
│   └── plans/                       # Execution plans + archive
├── CLAUDE.md                        # Auto-loaded solver workflow docs
├── .env.example
└── launch_worktree.py
```

## 5. Solver Loop Flow (Harness-as-Solver)

```
┌─────────────────────────────────────────────────────┐
│              Claude Code Session                     │
│        (reasoning, strategy, evaluation)             │
└──────────────────────┬──────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
   ┌──────────┐ ┌───────────┐ ┌──────────┐
   │ /research │ │ /plan auto│ │/orchestr.│
   │ (analyze) │ │ (build)   │ │(parallel)│
   └─────┬────┘ └─────┬─────┘ └────┬─────┘
         │            │             │
         ▼            ▼             ▼
   ┌──────────────────────────────────────┐
   │         Subagent (Agent tool)        │
   │   Runs Python scripts, returns      │
   │   summary to main context           │
   └──────────────────┬──────────────────┘
                      │
         ┌────────────┼────────────┐
         │            │            │
         ▼            ▼            ▼
   ┌──────────┐ ┌──────────┐ ┌──────────┐
   │ scripts/ │ │ docs/    │ │ docs/    │
   │ *.py     │ │converge/ │ │deferred/ │
   │(compute) │ │ (log)    │ │(triage)  │
   └──────────┘ └──────────┘ └──────────┘
```

### Single Iteration Flow

1. **Research** — `/mindcoachlabs:research` analyzes the problem, identifies approach
2. **Plan** — `/mindcoachlabs:plan auto` creates a plan to test the approach
3. **Build (subagent)** — Writes/runs a Python script via Agent tool, evaluates results
4. **Log** — `scripts/log_convergence.py` appends JSONL entry with findings
5. **Triage** — `/mindcoachlabs:triage` reviews dead ends, updates deferred items
6. **Decide** — Claude evaluates convergence; if not solved, feed findings into step 1
7. **Track issues** — Log any autonomy blockers to `docs/orchestration-issues.md`

### Context Preservation Strategy

- **Main session**: Reasoning, strategy selection, evaluation, harness commands
- **Subagents**: Run Python scripts, grep/search, heavy computation — output stays in subagent, only summary returns to main
- **Convergence logs**: Persist findings across sessions (repo-tracked JSONL)
- **Research archives**: Persist detailed analysis across sessions (docs/research/)

## 6. Configuration

No `.env` required for the solver workflow. Python scripts use only sympy (stdlib-compatible).

Optional: `scripts/requirements.txt` lists `sympy` for computation scripts.

## 7. Cross-references

- Convergence tracking schema: `docs/design/convergence-tracking.md`
- Orchestration issues: `docs/orchestration-issues.md`
- Research artifacts: `docs/research/`
- Deferred approaches: `docs/deferred/index.md`
