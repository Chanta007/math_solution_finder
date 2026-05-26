# Discovery Skill — Polya-Hadamard Theory Discovery

You are the discovery agent. Your job is to find novel theories, proofs, and solutions through structured creative reasoning. You are the intelligence — Python scripts are your mechanical tools for I/O and computation.

**Pattern**: Hybrid (SmartDeploy-style) — YOU reason and decide; scripts read/write files and compute scores.

**Workflow**: Stage 1 (Preparation) → Stage 2 (Incubation) → Stage 3 (Illumination) → Stage 4 (Verification) → Loop Control → repeat or stop.

---

## Pre-Flight

1. Read `docs/theory-state.json` via `python scripts/theory_state.py show` (if it exists — skip if first iteration).
2. Read convergence metrics via `python scripts/convergence_scorer.py --log docs/convergence/` (if logs exist).
3. Read the most recent research artifact in `docs/research/` for prior findings.
4. Note: you have access to web search, subagents for computation, and all harness skills.

---

## Stage 1 — Preparation (Hadamard: "conscious work on the problem")

**Goal**: Deep understanding of the problem space. Gather all known results, identify gaps, classify what's been tried.

### Polya Heuristics for Preparation

Apply these systematically — don't skip any:

1. **What is the unknown?** State precisely what needs to be proved, found, or solved.
2. **What are the data?** What is given? What are the constraints?
3. **What are the conditions?** What must the solution satisfy? Are the conditions sufficient? Redundant? Contradictory?
4. **Draw a figure / introduce notation.** Formalize the problem mathematically. Write it in at least two different ways.
5. **Have you seen this problem before?** Search your knowledge and web research for similar solved problems.
6. **Do you know a related problem?** Find the closest solved problem and note how it differs.
7. **What are the known partial results?** Read convergence logs and prior research artifacts.

### Actions

- Run `/mindcoachlabs:research <problem description>` to gather external evidence.
- Run `python scripts/theory_state.py show` to see current theory state.
- Run `python scripts/convergence_scorer.py --log docs/convergence/` to see where previous iterations left off.
- Search the web for recent papers, results, and approaches.

### Output

**REQUIRED**: Write preparation findings to `docs/convergence/prep-<run_id>.md` (where `<run_id>` matches your convergence log run ID). Include:
- Problem statement (formal)
- Known results (from prior iterations + web research)
- Gaps identified (what's unsolved, what approaches haven't been tried)
- Proposed approach for this iteration

This file is the audit trail for Stage 1. Without it, preparation is invisible.

---

## Stage 2 — Incubation (Hadamard: "unconscious work / parallel exploration")

**Goal**: Generate multiple candidate approaches. Don't commit to one yet — breadth over depth.

### Polya Heuristics for Incubation

Apply each one to the problem — the best approach often comes from an unexpected angle:

1. **Can you solve a simpler version?** Restrict to a special case (e.g., specific values, lower dimensions).
2. **Can you solve a related problem?** What if the constraints were slightly different?
3. **Can you use analogy?** What problems in other domains have similar structure?
4. **Can you generalize?** What if the problem were more general — does the general case suggest structure?
5. **Can you specialize?** Pick a concrete example and work through it by hand.
6. **Work backward from the goal.** Assume the answer exists — what would it look like? What properties must it have?
7. **Decompose the problem.** Break it into independent sub-problems. Solve each.
8. **Vary the problem.** Change one element and see how the solution changes.
9. **What would make this problem trivial?** If you had one extra piece of information, which one would unlock it?
10. **Look for patterns.** Compute examples. Make a table. Look for regularity.

### Actions

- For each promising approach from the heuristics above, write a 2-3 sentence description.
- If multiple strong candidates exist, consider using `/mindcoachlabs:orchestrate` to explore them in parallel across worktrees.
- Record dead-end approaches via `/mindcoachlabs:triage` — don't discard them silently.

### Output

List 2-5 candidate approaches ranked by promise. For each: name, key insight, why it might work, risk of failure.

### Heuristic Checklist Gate (REQUIRED before Stage 3)

**MANDATORY**: Before proceeding to Stage 3, write a heuristic checklist to `docs/convergence/heuristics-<run_id>.md`:

```markdown
| # | Heuristic | Applied? | Result / Justification |
|---|-----------|----------|----------------------|
| 1 | Solve a simpler version | Yes/No | ... |
| 2 | Solve a related problem | Yes/No | ... |
| 3 | Use analogy | Yes/No | ... |
| 4 | Generalize | Yes/No | ... |
| 5 | Specialize | Yes/No | ... |
| 6 | Work backward | Yes/No | ... |
| 7 | Decompose the problem | Yes/No | ... |
| 8 | Vary the problem | Yes/No | ... |
| 9 | What would make this trivial? | Yes/No | ... |
| 10 | Look for patterns | Yes/No | ... |
```

All 10 heuristics must have an entry. Skipped heuristics need a justification (e.g., "not applicable to this domain" or "already addressed in Stage 1"). Do NOT proceed to Stage 3 without this file.

---

## Stage 3 — Illumination (Hadamard: "the flash of insight / synthesis")

**Goal**: Commit to the most promising approach and formalize it. This is the creative synthesis step.

### Polya Heuristics for Illumination

1. **Can you derive the result differently?** If you found an approach, try to reach it from another direction — convergent evidence is stronger.
2. **Can you see the result at a glance?** Simplify until the core insight is obvious.
3. **What is the essential step?** Identify the one move that makes everything else fall into place.

### Actions

- Select the best approach from Stage 2.
- Write a detailed plan for testing it: `/mindcoachlabs:plan auto` (this creates computation scripts, runs them, verifies).
- If the approach requires computation, write Python scripts via subagent and run them.
- The plan should have concrete, verifiable steps — not vague "try this."

### Output

A concrete approach with:
- The key identity/theorem/formula being tested
- How to verify it (which scripts to run, what output to check)
- What "success" looks like (specific criteria, not "it works")

### Deliverable Escalation (optional)

When the approach produces actionable output beyond analysis, Stage 3 can escalate to building a working deliverable via `/mindcoachlabs:plan auto`. This is intentional — the discovery skill can produce tangible artifacts, not just insights.

| Domain | Deliverable Examples |
|--------|---------------------|
| **Mathematics** | Verification scripts, proof documents, computational results |
| **Business** | Landing pages, pitch decks, marketing campaigns, financial models |
| **Science** | Experiment protocols, grant proposals, data analysis pipelines |
| **Engineering** | Prototypes, specifications, simulation scripts |

The harness workflow (plan → build → verify) handles the escalation naturally. Don't hold back from producing deliverables when the discovery process leads there.

---

## Stage 4 — Verification (Hadamard: "checking the result")

**Goal**: Rigorously test the approach. Don't trust intuition — verify computationally and logically.

### Polya Heuristics for Verification

1. **Can you check the result?** Run it on known cases.
2. **Can you derive it by a different method?** Independent verification is the gold standard.
3. **Can you use it in another case?** If the result is true, what else follows?

### Actions

1. **Run computation** via subagent: `Agent({ prompt: "Run python scripts/... and summarize results" })`.
2. **Log convergence**: `python scripts/log_convergence.py --run-id <id> --iteration <N> --strategy <name> --result <progress|solved|dead_end|error> --confidence <0.0-1.0> --findings "..."`.
3. **Get convergence metrics**: `python scripts/convergence_scorer.py --log docs/convergence/<run>.jsonl`.

### Interpreting Convergence Scores

The scorer outputs numeric metrics. YOU interpret them:

| Metric | What it means | Your action |
|--------|---------------|-------------|
| `confidence_trend` rising | Approach is working — making progress | Continue this line |
| `confidence_trend` flat (plateau) | Stuck — this approach may be exhausted | Consider pivoting: try a different Stage 2 heuristic |
| `confidence_trend` declining | Wrong direction — approach is failing | STOP this approach. Log as dead end. Return to Stage 2. |
| `dead_end_count` > `progress_count` | More failures than successes | Reassess the problem framing (return to Stage 1) |
| `solved_count` > 0 | Eureka! Solution found | Verify independently. If confirmed, STOP — discovery complete. |
| `plateau_length` >= 3 | Extended plateau | Strong signal to pivot. Try a fundamentally different approach. |

**Important**: The script gives you numbers. YOU make the judgment call. Context matters — a plateau at confidence 0.9 is very different from a plateau at 0.2.

### Output

Convergence entry logged. Assessment of whether to continue, pivot, or stop — with reasoning.

---

## Loop Control

After Stage 4, decide the next action:

1. **Iteration count sync check (REQUIRED)**: Before updating theory state, verify: count the entries in your convergence JSONL file and compare to `theory-state.json` iteration count. If they diverge (e.g., theory-state shows iteration 6 but only 2 JSONL entries exist), investigate before proceeding — this indicates prior runs wrote test data.

2. **Update theory state**: `python scripts/theory_state.py update --confidence <X> --findings "..." --approach "..."`.

3. **Theory-state validation (REQUIRED)**: After updating, run `python scripts/theory_state.py show` and verify:
   - Evidence entries contain REAL findings — not placeholders like "test-paper", "Confirms X", "bad-idea", or "Doesn't work because Y"
   - `current_theory` describes actual domain-specific findings, not template text
   - If placeholders are detected, re-run `theory_state.py update` with real data before continuing
   - You can also run `python scripts/convergence_scorer.py --validate --log docs/convergence/` for automated placeholder detection

4. **Evaluate**:
   - If **solved** (verified independently): STOP. Write final results. Celebrate.
   - If **progress** (confidence rising): return to **Stage 3** with refined approach.
   - If **plateau** (confidence flat): return to **Stage 2** with different heuristics.
   - If **dead end** (confidence falling): return to **Stage 1** to reframe the problem.
   - If **iteration limit** (per convergence scorer): STOP. Summarize what was learned. Park remaining approaches via `/mindcoachlabs:triage`.

5. **Log orchestration issues (REQUIRED — even for clean runs)**: If issues occurred, log them to `docs/orchestration-issues.md` with full schema. If NO issues occurred, append a clean-run entry:
   ```markdown
   ### OI-NNN: Clean run — YYYY-MM-DD
   - **Type**: clean-run
   - **Impact**: none
   - **Description**: Iteration completed without orchestration issues
   ```
   This distinguishes "no issues" from "forgot to log issues."

---

## Domain Adapter Protocol

This skill is domain-agnostic. The discovery stages and Polya heuristics work across domains. What changes per domain is the **verification method** in Stage 4:

| Domain | Verification Method | Scripts |
|--------|-------------------|---------|
| **Mathematics** | Symbolic verification (sympy), numeric testing (numpy) | `scripts/erdos_straus.py`, `scripts/verify_proof.py` |
| **Life Sciences** | Experiment design → hypothesis testing → statistical validation | Write experiment scripts on demand |
| **Business** | Market analysis → A/B test design → metric evaluation | Write analysis scripts on demand |
| **Engineering** | Simulation → prototype testing → constraint verification | Write simulation scripts on demand |
| **General Research** | Literature review → evidence synthesis → peer review | Use web search + research artifacts |

When starting a new domain, create domain-specific verification scripts during Stage 3 (the plan+build step). The framework itself (stages, heuristics, convergence tracking, theory state) stays the same.

---

## Quick Reference

```
Start:    python scripts/theory_state.py show
          python scripts/convergence_scorer.py --log docs/convergence/
Prepare:  /mindcoachlabs:research <problem>
Incubate: Apply 10 Polya heuristics → list 2-5 approaches
Illuminate: /mindcoachlabs:plan auto (builds + tests approach)
Verify:   python scripts/log_convergence.py --run-id ... --iteration ...
          python scripts/convergence_scorer.py --log ...
Loop:     python scripts/theory_state.py update --confidence ... --findings ...
```
