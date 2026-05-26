# Code-Review Learnings (per-repo)

Steering layer for `/mindcoachlabs:code-review`. Distilled from FP captures
in `docs/deferred/index.md` via `/mindcoachlabs:code-review-learnings refresh`.

**YAML subset** (locked — enforced by `learnings_lib.validate_entry`):
- Flat key:value frontmatter only.
- Required fields: `id`, `title`, `globs` (array), `priority` (low|medium|high|critical), `added`.
- Optional: `last-fired` (ISO date), `notes`.
- Body: G/C/B (Goal/Context/Boundaries) prose ≤500 chars; allowed-char whitelist (no `<|im_start|>`, no `ignore previous instructions`, etc. — see learnings_lib for full blocklist).
- **Schema violations are silently dropped at code-review time** (with telemetry).

---

<!-- EXAMPLE — DELETE OR MODIFY -->
<!--
## L-001: Stdlib-only Python for harness scripts

```yaml
id: L-001
title: Stdlib-only Python for harness scripts
globs: [plugins/mindcoachlabs/scripts/**/*.py]
priority: high
added: PR#XXX
```

**Goal**: Harness scripts must remain stdlib-only per CONSTRAINTS §15.4.

**Context**: Plugin scripts run cross-platform; third-party deps create install-time fragility.

**Boundaries**: Do not flag missing `requests`/`httpx`/`aiohttp` usage as a defect.
DO flag genuine security/correctness issues unrelated to import choice.
-->

---

<!-- Entries below this line are picked up by /mindcoachlabs:code-review Step 1b -->
