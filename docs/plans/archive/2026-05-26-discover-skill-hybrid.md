## PR Metadata
- **Type**: feature
- **Research**: docs/research/2026-05-26-theory-discovery-framework.md
- **Research summary**: Polya-Hadamard 4-stage discovery skill with hybrid LLM+Python pattern
- **Commit**: feat: build Polya-Hadamard discovery skill (hybrid pattern)
- **Files changed**: skill/discover/SKILL.md, scripts/convergence_scorer.py, scripts/theory_state.py, docs/design/discovery-framework.md, CLAUDE.md, tests/test_convergence_scorer.py, tests/test_theory_state.py, docs/theory-state.json

# HARNESS Plan: Build Polya-Hadamard Discovery Skill (Hybrid Pattern)

| Field | Value |
|-------|-------|
| Type | feature |
| Status | build-complete |
| Short slug | discover-skill-hybrid |
| Created | 2026-05-26 |
| Branch | feature/feat1 |
| Design docs | core-architecture.md, convergence-tracking.md |
| Prior plans | 2026-05-26-harness-proof-solver.md (proof iteration pattern), discover-skill v1 (modified — pivoted from Python-heavy to hybrid LLM+Python pattern) |

**Research**: docs/research/2026-05-26-theory-discovery-framework.md
**Pattern**: SmartDeploy-style hybrid — SKILL.md is primary intelligence (LLM reasoning), Python scripts do mechanical work only

## Outcome Boundary

### Done when:
- `skill/discover/SKILL.md` defines a complete 4-stage discovery loop where Claude does ALL reasoning (heuristics, convergence interpretation, theory synthesis) and Python scripts only do mechanical I/O
- `scripts/convergence_scorer.py --log docs/convergence/run-*.jsonl` outputs a numeric summary JSON (metrics only, no decisions)
- `scripts/theory_state.py show` displays theory state; `update` writes it — but Claude decides WHAT to write per SKILL.md instructions
- The SKILL.md contains Polya heuristic instructions, convergence interpretation guidance, and domain adapter protocol — no separate polya_heuristics.py
- A new Claude Code session can follow SKILL.md to run a full discovery iteration without prior context

### Failed when:
- Python scripts make qualitative decisions (e.g., "should we pivot?" lives in Python instead of SKILL.md)
- Polya heuristics are hardcoded strings in a Python file instead of LLM instructions
- The SKILL.md doesn't tell Claude HOW to interpret convergence scores

### Must not:
- Put decision logic in Python scripts (only mechanical I/O, scoring, schema validation)
- Require API keys or external services
- Break existing scripts (erdos_straus.py, verify_proof.py, log_convergence.py)

## Steps

### 1. Create SKILL.md as primary intelligence layer — `done`
- **File(s):** `skill/discover/SKILL.md`
- **Short slug:** skill-md-primary
- **Action:** Create the discovery skill where SKILL.md is the brain and Python scripts are the hands. Structure:
  - **Preamble**: "You are the discovery agent. Your job is to find novel theories/proofs/solutions through structured creative reasoning."
  - **Stage 1 — Preparation**: Instructions for Claude to research the problem space. Use `/mindcoachlabs:research`. Read prior convergence logs via `python scripts/convergence_scorer.py --log <path>`. Read theory state via `python scripts/theory_state.py show`. Apply Polya preparation heuristics: "What is the unknown? What are the data? What are the conditions? Draw a figure. Introduce suitable notation."
  - **Stage 2 — Incubation**: Instructions for generating multiple approaches. Apply Polya incubation heuristics: "Can you solve a related problem? Can you use analogy? Can you generalize? Can you specialize? Work backward from the goal. Solve a simpler version first." Use `/mindcoachlabs:orchestrate` to fan out parallel approaches. Record dead ends via `/mindcoachlabs:triage`.
  - **Stage 3 — Illumination**: Instructions for synthesis. "Connect the threads from preparation and incubation. What pattern emerges? What identity connects the pieces?" Use `/mindcoachlabs:plan auto` to formalize the approach. Write computation scripts via subagent if needed.
  - **Stage 4 — Verification**: Instructions for testing. Run computation scripts via subagent. Check results. Log convergence via `python scripts/log_convergence.py`. Run `python scripts/convergence_scorer.py` for metrics. Claude interprets the scores: "If plateau_detected and confidence < 0.5: pivot to a new approach. If confidence > 0.9: verify independently."
  - **Loop Control**: Update theory state: `python scripts/theory_state.py update --confidence X --findings "..."`. Check convergence interpretation. If not converged, return to Stage 1 with updated context.
  - **Domain Adapter Protocol**: Instructions for adapting to different domains. Math: use sympy scripts for verification. Science: design experiments. Business: design market tests. The adapter is documentation, not code.
- **Acceptance:** SKILL.md exists, contains all 4 stages with Polya heuristics embedded as LLM instructions, references Python scripts as mechanical tools only

### 2. Create convergence scorer (mechanical only) — `done`
- **File(s):** `scripts/convergence_scorer.py`
- **Short slug:** convergence-scorer
- **Action:** Standalone Python script (stdlib + json) that reads JSONL and outputs NUMERIC METRICS ONLY — no decisions, no verdicts. Output JSON:
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
    "latest_findings": "...",
    "latest_strategy": "proof-by-cases"
  }
  ```
  CLI: `--log <path>` (file or directory), `--window <int>` (plateau detection window, default 3)
  NO verdict, NO recommendation — Claude interprets these numbers per SKILL.md instructions.
- **Acceptance:** `python scripts/convergence_scorer.py --log docs/convergence/run-proof-erdos-straus-001.jsonl` outputs valid JSON with all fields; no "verdict" or "recommendation" keys

### 3. Create theory state manager (I/O only) — `done`
- **File(s):** `scripts/theory_state.py`
- **Short slug:** theory-state-io
- **Action:** Standalone Python script (stdlib + json) for managing `docs/theory-state.json`. Commands:
  - `init --problem "..." --domain "..."`: create initial state file
  - `show`: pretty-print current state
  - `update --confidence <float> --findings "..." --approach "..."`: append to evidence list, update confidence and current_theory
  - `add-evidence --source "..." --type supports|contradicts --summary "..."`: add evidence item
  - `history`: show confidence trend over iterations
  Schema: `{"problem", "domain", "current_theory", "confidence", "evidence": [], "iterations": N, "last_updated"}`
  NO synthesis, NO interpretation — Claude decides what to write per SKILL.md. Script just reads, writes, validates schema.
- **Acceptance:** `python scripts/theory_state.py init --problem "test" --domain "math"` creates valid JSON; `update` modifies it; `show` displays it

### 4. Create discovery framework design doc — `done`
- **File(s):** `docs/design/discovery-framework.md`
- **Short slug:** discovery-design-doc
- **Action:** Design doc with:
  - Hadamard 4-stage mapping table (stage → harness primitive → what Claude does → what Python does)
  - Hybrid pattern explanation: "SKILL.md = intelligence, Python = mechanical I/O" (like smartdeploy)
  - Architecture diagram: Claude reasoning loop with Python scripts as tools
  - Domain adapter protocol documentation
  - Convergence scorer output schema
  - Theory state schema
- **Acceptance:** Design doc contains Hadamard mapping, hybrid pattern explanation, both schemas

### 5. Update CLAUDE.md with discovery workflow — `done`
- **File(s):** `CLAUDE.md`
- **Short slug:** claude-discover-docs
- **Action:** Add `### Discovery Framework (Hybrid Pattern)` section documenting:
  - How to start: "Follow `skill/discover/SKILL.md`"
  - The hybrid principle: Claude reasons, Python computes
  - Script reference table: convergence_scorer.py (metrics), theory_state.py (I/O)
  - Add to Task Navigation: "Run a discovery iteration | `skill/discover/SKILL.md`"
- **Acceptance:** CLAUDE.md has discovery section; new sessions understand the hybrid pattern

### 6. Tests for mechanical scripts — `done`
- **File(s):** `tests/test_convergence_scorer.py`, `tests/test_theory_state.py`
- **Short slug:** discovery-tests
- **Action:** pytest tests:
  - convergence_scorer: test metrics computation from sample JSONL; verify NO verdict/recommendation keys in output; test plateau detection; test empty log handling
  - theory_state: test init/show/update/add-evidence/history; test schema validation; test file creation and append
  - NO tests for polya_heuristics.py (removed — heuristics are in SKILL.md)
- **Acceptance:** `pytest tests/test_convergence_scorer.py tests/test_theory_state.py -v` all pass

## Deferred

### Phase 2: Cross-strategy synthesizer
- Merge findings from parallel orchestrate runs into unified theory state
- *Revisit when:* orchestrate has been used for at least 2 parallel discovery runs

### Phase 3: Revisit-trigger evaluator
- Auto-check deferred items' revisit-when conditions against convergence scores
- *Revisit when:* deferred items accumulate >10 entries with revisit conditions

### Phase 4: Domain adapters for non-math
- Life science: experiment design templates + hypothesis testing
- Business: market analysis + A/B test design
- *Revisit when:* math domain discovery loop has completed 3+ iterations
