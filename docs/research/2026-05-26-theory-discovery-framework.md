# Theory Discovery Framework Architecture

**Date**: 2026-05-26
**Slug**: theory-discovery-framework
**Status**: approved

---

## Question

How should we build a general-purpose "theory discovery" skill/framework for Claude Code + MindCoachLabs harness that can generate novel theories, proofs, and solutions — starting with hard theoretical math problems (like Guo's Erdős–Straus proof), then applicable to simpler domains (college assignments, business problems, life sciences, robotics)? The user wants to start by replicating how humans discover theories, then enhance with LLM capabilities in Phase 2.

## Thinking — How We Got Here

### Initial framing & gut intuition

The first instinct was to build something like AlphaProof — a formal verification loop with RL-trained proof generation. But that requires Lean 4 expertise and massive compute. The user's insight was sharper: start by understanding how humans actually discover things (Polya, Hadamard), replicate that process with existing harness tools, then enhance.

### Pivots during research

Two major pivots:
1. **Hadamard's 4-stage model maps perfectly to harness skills.** Preparation = `/mindcoachlabs:research`. Incubation = `/mindcoachlabs:orchestrate` (parallel exploration) + `/mindcoachlabs:triage` (deferred items percolating). Illumination = `/mindcoachlabs:plan` (the moment of synthesis). Verification = `/mindcoachlabs:verify` + Python scripts. The framework is already 70% built.
2. **The verification bottleneck is the key leverage point.** Multiple sources (AI-Descartes, POPPER, Hilbert) confirm that hypothesis generation now outpaces validation. The framework's differentiator should be automated verification — currently our strongest primitive (sympy scripts, convergence tracking).

### Options we considered and rejected

- **Full AI Scientist pipeline** — too ambitious for Phase 1. Requires experiment infrastructure per domain, costs hundreds of iterations. Better as a Phase 3 aspiration once the basic loop works.
- **Pure formal verification (Lean 4)** — too domain-specific. Great for math but useless for business problems or life sciences. The framework must be domain-agnostic.

### Open empirical questions deliberately not answered here

1. **Can "incubation" be replicated without unconscious processing?** Hadamard's model relies on unconscious pattern matching. Our substitute — parallel exploration via orchestrate + deferred items percolating via triage — is a reasonable proxy but untested.
2. **Does the framework scale down?** Starting with hard math and applying to college assignments may reveal that simpler problems don't need the full pipeline. The framework needs graceful degradation.
3. **What's the right convergence metric across domains?** Math has proof verification. Life sciences has experimental validation. Business has market results. The convergence tracker schema may need domain-specific extensions.
4. Adversarial check: searched for "LLM cannot replicate human mathematical intuition"; found evidence that ML-guided intuition is effective and the reasoning gap is closing (DeepMind 2025-2026). Clear.

## Options Considered

| Option | Pros | Cons | Cost |
|--------|------|------|------|
| **A. Polya-Hadamard Discovery Skill** | Maps to human discovery process (Hadamard 4 stages, Polya heuristics); uses existing harness primitives; domain-agnostic; user's preferred "replicate then enhance" approach; smallest build cost | No formal verification; "incubation" proxy untested; may be too structured for genuine novelty | Small — compose existing skills + 6 new components |
| **B. FunSearch Evolutionary Loop** | Proven genuine discoveries (cap set problem, Nature 2024); evolutionary pressure finds solutions humans miss; natural fit for orchestrate | Requires well-defined evaluation functions per domain; heavy compute; less interpretable than structured reasoning | Medium — custom evaluation harness per domain |
| **C. AI Scientist Full Pipeline** | Most ambitious; autonomous end-to-end research; proven at conference level (Sakana Nature 2025); v2 eliminates human templates | Massive scope; months of work; $15/paper × hundreds of iterations; overkill for Phase 1 | Large |
| **D. Neuro-Symbolic Hybrid** | Strongest correctness (AI-Descartes/Hilbert pattern); KG prevents hallucination; 26.5% improvement over CoT | Requires Lean 4 for math; KG infrastructure overhead; most complex; not domain-agnostic without per-domain ontologies | Large |

## Decision + Rationale

**Recommended: Option A (Polya-Hadamard Discovery Skill) with FunSearch-style parallel generation for the "incubation" stage.**

The framework is a new `/mindcoachlabs:discover` skill that implements Hadamard's 4-stage discovery process by composing existing harness primitives:

| Hadamard Stage | Harness Mapping | What It Does |
|---|---|---|
| **1. Preparation** | `/mindcoachlabs:research` + literature mining | Deep problem analysis, survey known results, identify gaps |
| **2. Incubation** | `/mindcoachlabs:orchestrate` + `/mindcoachlabs:triage` | Parallel exploration of approaches across worktrees; deferred items "percolate" as conditions change |
| **3. Illumination** | `/mindcoachlabs:plan` (synthesis step) | Connect findings into a novel approach; the "aha" moment is the plan that synthesizes disparate threads |
| **4. Verification** | `/mindcoachlabs:build` + `/mindcoachlabs:verify` + Python scripts | Test the approach computationally; verify symbolically; log convergence |

The 6 missing components to build:
1. **Convergence automator** — evaluates convergence criteria after each iteration (replaces manual decision)
2. **Cross-strategy synthesizer** — merges findings from parallel orchestrate runs
3. **Revisit-trigger evaluator** — checks if deferred items' revisit-when conditions are met
4. **Theory state tracker** — maintains the current best-guess theory/conjecture as evidence accumulates
5. **Polya heuristic prompter** — generates analogy/generalization/specialization prompts from Polya's 67 heuristics
6. **Domain adapter** — maps abstract discovery stages to domain-specific actions (math: sympy verification; life science: experiment design; business: market testing)

This recommendation is grounded in multiple evidence lines: Hadamard's model is the foundational framework for understanding mathematical discovery (preparation→incubation→illumination→verification); Polya's heuristics provide the concrete operational moves within each stage; TRIZ demonstrates that the same pattern-extraction approach works across engineering domains; and the codebase analysis shows 5 of 6 discovery stages already have harness primitives — only the 6 components listed above need building.

Phase 2 enhancement path: once the basic loop works, add FunSearch-style evolutionary generation (Option B elements) for the incubation stage, and knowledge graph grounding (Option D elements) for the preparation stage.

## Evidence

### External

**Hadamard (1945)**: "The roots of creativity lie not in consciousness, but in the long unconscious work of incubation." Four-stage model: preparation, incubation, illumination, verification. (Princeton University Press)

**Polya (1945)**: Four phases: understand, plan, execute, look back. 67 heuristic concepts including analogy, decomposition, generalization, specialization. "Altshuller's TRIZ methods in many aspects reproduces or parallels Polya's work." (Wikipedia)

**Thurston (1994)**: "What mathematicians most wanted was to learn my ways of thinking, not my proof." Mathematical understanding is social and cognitive. (math.toronto.edu/mccann/199/thurston.pdf)

**AlphaProof (DeepMind, Nature 2025)**: RL + Lean 4 formal verification. Silver medal at IMO 2024. "Every step is machine-checked." (Nature)

**FunSearch (DeepMind, Nature 2024)**: "Pairing LLM with automated evaluator. Initial solutions evolve into new knowledge." Made largest cap set improvement in 20 years. (deepmind.google/discover/blog/funsearch)

**Hilbert (Apple, 2025)**: "Orchestrates four components: informal LLM, specialized prover LLM, formal verifier, semantic theorem retriever." 99.2% on miniF2F. (machinelearning.apple.com/research/hilbert)

**AI Scientist v2 (Sakana, 2025)**: "Progressive agentic tree-search. First fully AI-generated paper to exceed human acceptance threshold." (arXiv:2504.08066)

**TRIZ (Altshuller)**: "Only about 100 fundamental ways to solve any problem." 40 Inventive Principles from 40,000 patent abstracts. (triz.co.uk)

**Knowledge Graphs for LLM Reasoning (2025)**: "Grounding turns intermediate 'thoughts' into interpretable traces. At least 26.5% improvement over CoT." (arXiv:2502.13247)

**AI-Descartes (2023)**: "Laws can be discovered from few data points when using formal logical reasoning to distinguish correct formula from plausible ones." Derived Kepler's law, Einstein's time-dilation. (arXiv:2109.01634)

**Verification Bottleneck (2025)**: "Hypotheses can be rapidly produced but verification still relies on slow, manual evaluation." (arXiv:2509.01398)

**POPPER (2025)**: "Comparable performance to human scientists in validating hypotheses while reducing time by 10 folds." (arXiv:2502.09858)

**DeepMind Grand Challenge (2026)**: Gold-medal IMO 2025 performance. Using AlphaEvolve on Navier-Stokes singularities. "Era of autonomous discovery has arrived." (Multiple sources)

### Internal patterns referenced

- Existing harness-as-solver workflow (CLAUDE.md §Solver Workflow) — research → plan auto → subagent computation → convergence log → triage
- Convergence tracking schema (docs/design/convergence-tracking.md) — JSONL with confidence, path branching, dead-end tracking
- Orchestrate skill — fans out parallel approaches across worktrees
- Triage + deferred items (docs/deferred/index.md) — ICE-scored parked approaches with revisit-when triggers
- Research archives (docs/research/) — chained research with predecessor links
- Iteration 1 convergence log (run-proof-erdos-straus-001.jsonl) — demonstrates the loop in practice

### Source tensions

1. **Formal verification vs. creative exploration**: AlphaProof requires Lean 4 formal proofs (guaranteed correctness); FunSearch uses informal LLM generation + empirical evaluation (faster, more creative, less rigorous). The framework must balance both — formal verification for math, empirical evaluation for other domains.
2. **Full autonomy vs. human understanding**: AI Scientist v2 is fully autonomous; Thurston argues value lies in communicating understanding. The Polya-Hadamard approach favors comprehensible reasoning over opaque solutions.

## Parked Future Angles

- **FunSearch evolutionary generation for incubation stage**: pair LLM generation with automated evaluation in an evolutionary loop. *Revisit when:* basic Polya-Hadamard discovery loop has completed 5+ iterations and convergence patterns are understood.
- **Lean 4 formal verification integration**: add formal proof checking for the math domain. *Revisit when:* the framework is working on math problems and informal verification (sympy) hits correctness limits.
- **Knowledge graph grounding (Neo4j/Weaviate)**: ground LLM reasoning in structured knowledge to prevent hallucination. *Revisit when:* the framework is applied to life sciences or other domains where factual grounding is critical.
- **AI Scientist full pipeline**: automate from ideation through paper writing. *Revisit when:* the basic discovery loop is proven on 3+ domains and the user wants fully autonomous research.
- **POPPER-style sequential hypothesis falsification**: statistical testing framework for experiment-driven domains. *Revisit when:* applying the framework to life sciences or experimental physics where hypothesis testing is the verification mechanism.

## Re-evaluation Hooks

1. **If the Polya-Hadamard loop fails to generate any novel insight after 10 iterations on Erdős–Straus**: the structured approach may be too rigid. Consider switching to FunSearch evolutionary generation (Option B) which has proven discovery ability.
2. **If the framework works on math but fails on the first non-math domain (e.g., business problem)**: the domain adapter component may be insufficient. Consider whether the framework needs domain-specific skill variants rather than a single generic skill.
