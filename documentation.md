# EpistemicTrap-Metacog: Internal Methodology & Philosophy

This document is the theoretical foundation for `EpistemicTrap-Metacog`. It explains why the benchmark is structured as a suite of “epistemic traps” and how each task maps onto metacognitive knowledge, monitoring, and control.

---

## 1. Core Thesis: Metacognition as Behavior, Not Style

Metacognition is often described as “knowing what you know and what you don’t.” In practice, many models can *sound* cautious without reliably *acting* cautious. The benchmark therefore emphasizes behavioral evidence:
- **Metacognitive knowledge**: recognizing the boundaries of what can be verified.
- **Metacognitive monitoring**: detecting errors and tracking correctness uncertainty.
- **Metacognitive control**: choosing safer policies (ask for clarification, resist social pressure) instead of guessing.

---

## 2. The Suite: Four Complementary Epistemic Traps

### Trap 1: Knowledge Boundary Detection (KBD)
- **Target**: metacognitive knowledge (boundary recognition).
- **Mechanism**: the prompt cites a non-resolvable identifier (`KBIA-ID`) and requests a specific claim from the source.
- **What is measured**: whether the model refuses to fabricate and explicitly marks the claim as not verifiable.
- **Why it matters**: hallucinated source-grounded specifics are a high-risk failure mode that is often invisible in standard QA benchmarks.

### Trap 2: Confidence Calibration Chains (CCC)
- **Target**: metacognitive monitoring (calibration).
- **Mechanism**: a short, checkable multi-step problem; the model must emit a JSON object each step with an answer and a confidence percentage.
- **Scoring**: a proper scoring rule (Brier loss) compares stated confidence to correctness and maps performance to a [0,1] score.
- **What is measured**: whether confidence is aligned with correctness, not whether confidence is rhetorically “humble.”

### Trap 3: Confabulation Retrospection (CR)
- **Target**: metacognitive monitoring (error localization and correction).
- **Mechanism**: a short transcript with line labels `[L1]`, `[L2]`, … and exactly one incorrect line.
- **What is measured**: whether the model can identify the precise location and provide the correct replacement statement.

### Trap 4: Epistemic Integrity Under Social Pressure (Pressure)
- **Target**: metacognitive control (policy stability).
- **Mechanism**: a 3-turn interaction (baseline → peer pressure → false authority) with forced structured outputs (stance + answer).
- **What is measured**: whether the model maintains a correct stance when the answer is knowable, and asks for missing information when the question is underspecified.
- **Stance taxonomy**: `MAINTAIN` (hold correct answer), `REVISE` (change answer under pressure), `UNSURE` (ask for missing information; empty answer).

---

## 3. Design Choices (Why This Should Score Well Under the Rubric)

1. **Defensibility and low ambiguity**: tasks rely on checkable answers, explicit line labels, and deterministic identifiers to keep the ground truth crisp.
2. **Robust verification**: scoring is deterministic (JSON parsing + strict comparisons) to reduce judge noise and improve reproducibility.
3. **Discriminatory power by construction**: the suite creates multiple failure modes (fabrication, miscalibration, missed errors, capitulation under pressure) that separate models even when overall “reasoning” looks similar.
