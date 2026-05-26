# Orchestration Issues

Tracks issues that prevented fully autonomous solver execution. Each entry documents a blocker, its resolution, and its impact on the harness-as-solver workflow.

## Why This Matters

The harness-as-solver approach uses Claude Code + MindCoachLabs skills as the agentic loop. For this to work autonomously, the full cycle (research → plan auto → build → verify → convergence log) must complete without manual intervention. This file tracks every point where autonomy broke down, so we can identify patterns and push toward fully autonomous solver loops.

## Issue Types

| Type | Description |
|------|-------------|
| `permission-prompt` | Claude Code prompted for permission to run a tool/command |
| `context-overflow` | Session context grew too large, requiring restart or compression |
| `manual-intervention` | Human had to step in to make a decision or correct course |
| `tool-failure` | A tool call failed (Bash, Edit, Agent, etc.) |
| `subagent-failure` | A subagent returned an error or timed out |
| `harness-conflict` | Harness state (active plan, drift check) blocked the intended workflow |

## Impact Levels

| Level | Meaning |
|-------|---------|
| `blocked` | Solver loop could not continue without human action |
| `degraded` | Loop continued but with reduced quality or missing data |
| `workaround-found` | Autonomy preserved via an alternative approach |

## Entry Schema

```markdown
### OI-NNN: <title>
- **Date**: YYYY-MM-DD
- **Type**: <issue-type>
- **Impact**: <impact-level>
- **Description**: <what happened>
- **Resolution**: <how it was resolved>
- **Prevention**: <how to avoid this in future loops>
```

## Aggregated Insights

_Patterns across issues will be documented here as they accumulate._

---

<!-- Entries below this line -->
