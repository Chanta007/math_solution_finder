# Discovery Framework

> Last updated: May 2026

## 1. Purpose

Defines the Polya-Hadamard theory discovery framework — a domain-agnostic skill for finding novel theories, proofs, and solutions using Claude Code as the reasoning engine and Python scripts as mechanical tools.

## 2. Key Files

| File | Responsibility |
|------|---------------|
| `skill/discover/SKILL.md` | Primary intelligence layer — Polya heuristics, convergence interpretation, stage transitions |
| `scripts/convergence_scorer.py` | Mechanical: reads JSONL, computes numeric metrics (no decisions) |
| `scripts/theory_state.py` | Mechanical: read/write/validate `docs/theory-state.json` (no synthesis) |
| `scripts/log_convergence.py` | Mechanical: append JSONL convergence entries |
| `docs/convergence/` | Append-only iteration logs (JSONL) |
| `docs/theory-state.json` | Current best-guess theory with evidence trail |

## 3. Architecture — Hybrid Pattern

```
┌─────────────────────────────────────────────────────┐
│           Claude Code (SKILL.md = brain)              │
│                                                       │
│  Polya heuristics → strategy selection → synthesis    │
│  convergence INTERPRETATION → loop control decisions  │
│  theory narrative → domain adaptation                 │
└──────────┬──────────────┬──────────────┬─────────────┘
           │              │              │
    ┌──────▼──────┐ ┌────▼────┐ ┌──────▼──────┐
    │ convergence │ │ theory  │ │    log      │
    │ _scorer.py  │ │_state.py│ │_convergence │
    │ (metrics)   │ │ (I/O)   │ │    .py      │
    └──────┬──────┘ └────┬────┘ └──────┬──────┘
           │              │              │
    ┌──────▼──────┐ ┌────▼────┐ ┌──────▼──────┐
    │ docs/       │ │ docs/   │ │ docs/       │
    │convergence/ │ │theory-  │ │convergence/ │
    │ (JSONL)     │ │state.json│ │ (JSONL)     │
    └─────────────┘ └─────────┘ └─────────────┘
```

**Principle**: SKILL.md is the intelligence. Python scripts are the hands. Claude reasons about what to do; scripts handle file I/O, numeric computation, and schema validation. This mirrors the smartdeploy pattern where the LLM provides qualitative assessment and scripts do mechanical scoring.

## 4. Hadamard 4-Stage Mapping

| Hadamard Stage | What Claude Does (SKILL.md) | What Python Does (scripts/) | Harness Skill |
|---|---|---|---|
| **Preparation** | Applies Polya heuristics (7 questions), reads theory state, identifies gaps | `convergence_scorer.py` computes metrics, `theory_state.py show` loads state | `/mindcoachlabs:research` |
| **Incubation** | Generates 2-5 candidate approaches using 10 Polya heuristics | None (this is pure reasoning) | `/mindcoachlabs:orchestrate` |
| **Illumination** | Selects best approach, formalizes into a testable plan | Domain scripts written on demand | `/mindcoachlabs:plan auto` |
| **Verification** | Interprets convergence scores, decides continue/pivot/stop | `log_convergence.py` writes JSONL, `convergence_scorer.py` computes metrics | `/mindcoachlabs:build` + `/mindcoachlabs:verify` |

## 5. Convergence Scorer Schema

Output (no decisions — metrics only):

```json
{
  "iterations_completed": 5,
  "latest_confidence": 0.72,
  "confidence_trend": [0.3, 0.5, 0.6, 0.72, 0.72],
  "plateau_detected": true,
  "plateau_length": 2,
  "strategies_tried": ["symbolic", "numeric", "proof-by-cases"],
  "dead_end_count": 1,
  "progress_count": 3,
  "solved_count": 0,
  "error_count": 0,
  "latest_findings": "...",
  "latest_strategy": "proof-by-cases"
}
```

## 6. Theory State Schema

```json
{
  "problem": "Erdős–Straus conjecture",
  "domain": "math",
  "current_theory": "Even n and n≡3(mod 4) proved via parametric identities",
  "confidence": 0.4,
  "evidence": [{"source": "...", "type": "supports|contradicts", "summary": "..."}],
  "approaches_tried": ["proof-by-residue-cases"],
  "dead_ends": [{"approach": "...", "reason": "..."}],
  "iteration": 1,
  "last_updated": "2026-05-26T..."
}
```

## 7. Domain Adapter Protocol

The framework is domain-agnostic. Verification method changes per domain:
- **Math**: sympy/numpy scripts (already built: `erdos_straus.py`, `verify_proof.py`)
- **Science**: experiment design scripts (written on demand per problem)
- **Business**: analysis scripts (written on demand per problem)

Domain scripts are created during Stage 3 (Illumination) via `/mindcoachlabs:plan auto`.

## 8. Cross-references

- Convergence tracking schema: `docs/design/convergence-tracking.md`
- Core architecture: `docs/design/core-architecture.md`
- Research: `docs/research/2026-05-26-theory-discovery-framework.md`
