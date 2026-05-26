## PR Metadata
- **Type**: feature
- **Research**: evaluation of 4 test runs (Erdős–Straus iter1/iter2, sqrt(2), ai_gateway GTM)
- **Commit**: feat: improve discovery skill with 6 evaluation-driven enhancements
- **Files changed**: skill/discover/SKILL.md, scripts/convergence_scorer.py, tests/test_convergence_scorer.py, docs/design/discovery-framework.md
# HARNESS Plan: Improve Discovery Skill from 4-Run Evaluation

| Field | Value |
|-------|-------|
| Type | feature |
| Status | build-complete |
| Short slug | improve-discover-skill |
| Created | 2026-05-26 |
| Branch | feature/feat1 |
| Design docs | discovery-framework.md, convergence-tracking.md |
| Prior plans | 2026-05-26-discover-skill-hybrid.md (original skill build) |

## Outcome Boundary

### Done when:
- SKILL.md contains all 6 improvements: theory-state validation, persistent prep/incubation artifacts, heuristic checklist gate, iteration sync, clean-run orchestration entry, escalation-to-deliverable documentation
- `python scripts/convergence_scorer.py --validate --log docs/convergence/` detects placeholder entries in theory-state.json
- Tests pass for the new --validate flag

### Failed when:
- Any of the 6 improvements is missing from SKILL.md
- The --validate flag doesn't catch "test-paper" or "Confirms X" placeholder entries

### Must not:
- Break existing convergence_scorer.py functionality (--log still works without --validate)
- Change the hybrid pattern (SKILL.md = intelligence, Python = mechanical)

## Steps

### 1. Update SKILL.md with 6 improvements — `done`
- **File(s):** `skill/discover/SKILL.md`
- **Short slug:** skill-improvements
- **Action:** Apply all 6 evaluation-driven improvements to SKILL.md:
  1. **Loop Control — theory-state validation**: After `theory_state.py update`, add instruction: "Run `python scripts/theory_state.py show` and verify: (a) evidence entries contain real findings, not placeholders like 'test-paper' or 'Confirms X', (b) current_theory describes actual mathematical/domain findings. If placeholders detected, re-run update with real data."
  2. **Stage 1 — persistent prep artifact**: Change "Write a brief preparation summary (in your response, not a file)" to "Write preparation findings to `docs/convergence/prep-<run_id>.md` with sections: Problem Statement, Known Results, Gaps Identified, Proposed Approach."
  3. **Stage 2 — heuristic checklist gate**: Add before Stage 3 entry: "Before proceeding to Stage 3, write a heuristic checklist to `docs/convergence/heuristics-<run_id>.md`: | # | Heuristic | Applied? | Result/Justification |. All 10 incubation heuristics must have an entry. Skipped heuristics must have a justification."
  4. **Loop Control — iteration sync**: Add pre-update check: "Before running `theory_state.py update`, verify: count entries in convergence JSONL matches theory-state.json iteration count. If they diverge, investigate before proceeding."
  5. **Loop Control — clean-run orchestration**: Add: "If no orchestration issues were encountered during this iteration, append to docs/orchestration-issues.md: `### OI-NNN: Clean run — <date>` with `- **Type**: clean-run` and `- **Impact**: none`. This distinguishes 'no issues' from 'forgot to log.'"
  6. **Stage 3 — escalation-to-deliverable**: Add new subsection after existing Stage 3 content: "### Deliverable Escalation (optional). When the approach produces actionable output beyond analysis, Stage 3 can escalate to building a working deliverable. Domain examples: Math: write verification scripts. Business: build landing pages, create pitch decks. Science: design experiment protocols, write grant proposals. Engineering: build prototypes, write specifications. This is intentional — the discovery skill can produce tangible artifacts, not just insights."
- **Acceptance:** SKILL.md contains all 6 additions; grep finds "prep-<run_id>.md", "heuristics-<run_id>.md", "theory_state.py show", "OI-NNN: Clean run", "Deliverable Escalation"

### 2. Add --validate flag to convergence_scorer.py — `done`
- **File(s):** `scripts/convergence_scorer.py`
- **Short slug:** validate-flag
- **Action:** Add `--validate` flag that reads `docs/theory-state.json` and checks for placeholder entries. Checks: (a) evidence entries containing "test-paper", "Confirms X", "bad-idea", "Doesn't work because Y" (b) empty current_theory field (c) iteration count mismatch with convergence JSONL. Output JSON adds `validation` key: `{"valid": true/false, "issues": ["placeholder evidence: 'test-paper'", ...]}`. Without --validate, behavior is unchanged.
- **Acceptance:** `python scripts/convergence_scorer.py --validate --log docs/convergence/` outputs JSON with `validation` key; detects placeholder entries in current theory-state.json

### 3. Tests for --validate flag — `done`
- **File(s):** `tests/test_convergence_scorer.py`
- **Short slug:** validate-tests
- **Action:** Add tests: test_validate_detects_placeholders (create theory-state with "test-paper" evidence, verify validation.valid=false), test_validate_clean_state (create clean theory-state, verify validation.valid=true), test_validate_iteration_mismatch (theory-state iter 6 but 2 JSONL entries, verify flagged).
- **Acceptance:** `pytest tests/test_convergence_scorer.py -v` all pass including new tests

### 4. Update design doc — `done`
- **File(s):** `docs/design/discovery-framework.md`
- **Short slug:** design-doc-update
- **Action:** Add section documenting the 6 improvements: persistent artifacts, heuristic gate, validation checks, clean-run logging, deliverable escalation. Update the Hadamard mapping table to include artifact outputs per stage.
- **Acceptance:** Design doc mentions all 6 improvements
