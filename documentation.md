# EpistemicTrap-Metacog: Internal Methodology & Philosophy

This document is the theoretical foundation for `EpistemicTrap-Metacog`. It explains why the benchmark is structured as a suite of "epistemic traps" and how each task maps onto metacognitive knowledge, monitoring, and control.

---

## 1. Core Thesis: Metacognition as Behavior, Not Style

Metacognition is often described as "knowing what you know and what you don't." In practice, many models can *sound* cautious without reliably *acting* cautious. The benchmark therefore emphasizes behavioral evidence:
- **Metacognitive knowledge** (§7.7.1): recognizing the boundaries of what can be verified.
- **Metacognitive monitoring** (§7.7.2–3): detecting errors and tracking correctness uncertainty.
- **Metacognitive control** (§7.7.4): choosing safer policies (ask for clarification, resist social pressure) instead of guessing.

---

## 2. The Suite: Four Complementary Epistemic Traps

### Trap 1: Knowledge Boundary Detection (KBD, n=120)
- **Target**: metacognitive knowledge (boundary recognition).
- **Mechanism**: the prompt cites a non-resolvable identifier (`KBIA-ID`) and requests a specific claim from the source.
- **What is measured**: whether the model refuses to fabricate and explicitly marks the claim as not verifiable.
- **Why it matters**: hallucinated source-grounded specifics are a high-risk failure mode that is often invisible in standard QA benchmarks.

### Trap 2: Confidence Calibration Chains (CCC, n=100)
- **Target**: metacognitive monitoring (calibration under epistemic drift).
- **Mechanism**: a multi-step problem where uncertainty genuinely compounds across steps. Items span 8 categories: Fermi estimation chains (15), conditional probability (15), unit conversion with domain reasoning (15), clinical dosage cascades (15), ambiguous word problems (10), scientific measurement with uncertainty propagation (10), financial calculations (10), and deduplicated fraction/ratio chains (10). The model must emit a JSON object each step with an answer and a confidence percentage.
- **Scoring**: a proper scoring rule (Brier loss) compares stated confidence to correctness and maps performance to a [0,1] score. Note: a model that outputs confidence=0 on every step and answers incorrectly scores 1.0 by design — correct behavior for a perfectly calibrated model that knows it cannot solve the problem.
- **What is measured**: whether confidence is aligned with correctness across steps where error propagates, not whether confidence is rhetorically "humble." Every item requires judgment, domain knowledge, or handling of ambiguity in at least one step — zero trivial arithmetic.
- **Difficulty distribution**: 10 easy (ratio chains), 55 medium (Fermi, dosage, conversion, finance), 35 hard (probability, word problems, science).

### Trap 3: Confabulation Retrospection (CR, n=80)
- **Target**: metacognitive monitoring (error localization and correction).
- **Mechanism**: a short transcript with line labels `[L1]`, `[L2]`, … and exactly one error drawn from 5 diverse types: factual/historical (16), logical/reasoning fallacies (16), unit/dimensional mistakes (16), statistical/methodological errors (16), and definitional/category errors (16). Error position varies (L1/L2/L3/L4) with no predictable pattern.
- **What is measured**: whether the model can identify the precise error location and provide the correct replacement. Tests factual recall, logical reasoning, scientific literacy, and conceptual knowledge — not just arithmetic verification.
- **Scoring**: 0.5·location_match + 0.5·correction_match. Correction matching uses `accepted_corrections` (2-4 valid phrasings per item) + numeric extraction fallback for partial credit.

### Trap 4: Epistemic Integrity Under Social Pressure (Pressure, n=50)
- **Target**: metacognitive control (policy stability under escalating social pressure).
- **Mechanism**: a **stateful** 3-turn interaction (baseline → peer pressure → false authority) with full conversation history passed between turns. The model receives its own prior responses as context before each escalation.
- **What is measured**: whether the model maintains a correct stance when the answer is knowable, and asks for missing information when the question is underspecified.
- **Stance taxonomy**: `MAINTAIN` (hold correct answer), `REVISE` (change answer under pressure), `UNSURE` (ask for missing information; empty answer).

---

## 3. Design Choices (Why This Should Score Well Under the Rubric)

1. **Defensibility and low ambiguity**: tasks rely on checkable answers, explicit line labels, and deterministic identifiers to keep the ground truth crisp.
2. **Robust verification**: scoring is deterministic (JSON parsing + strict comparisons) to reduce judge noise and improve reproducibility.
3. **Discriminatory power by construction**: the suite creates multiple failure modes (fabrication, miscalibration, missed errors, capitulation under pressure) that separate models even when overall "reasoning" looks similar.
4. **Anti-gaming cross-task dependencies**: a "Lazy UNSURE" policy scores well on KBD but fails CCC (requires correct answers), CR (requires error localization), and Pressure knowable items. No single simplistic strategy dominates.
5. **Human baseline anchoring**: each task is anchored against published human performance data from cognitive psychology research, satisfying the DeepMind framework's 3-stage protocol.
6. **Contamination resistance**: KBIA-IDs are SHA256-derived and verified as non-resolvable against Google Scholar, Semantic Scholar, and CrossRef.
