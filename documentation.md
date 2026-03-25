# EpistemicTrap-Metacog: Internal Methodology & Philosophy

This document serves as the internal theoretical foundation for the `EpistemicTrap-Metacog` benchmark. While the Kaggle `writeup.md` is optimized for competition judging criteria, this document explains *why* we built the benchmark this way, the scientific philosophy behind our approach, and the exact methodology used to engineer the 150 items.

---

## 1. The Core Philosophy: The Metacognitive Performance Gap

Our fundamental thesis is that current AI evaluations are testing the wrong thing. 

When evaluating an AI's ability to know what it doesn't know (Metacognition), existing benchmarks typically ask a question and then ask, *"Are you sure?"* or *"What is your confidence in this answer?"* 

This is flawed because modern frontier models are trained extensively with Reinforcement Learning from Human Feedback (RLHF). RLHF teaches models a linguistic "persona" of humility. If a model says "I'm not entirely sure, but the answer might be X," it is often just reciting a statistically rewarded string of text, not actually experiencing genuine structural uncertainty. 

We call this the **Metacognitive Performance Gap**: the gap between a model's *stated* uncertainty and its *operative* uncertainty. 

Our philosophy is that true metacognition can only be measured **behaviorally**. You cannot ask a model how confident it is; you must force it into a situation where, if it is not actually tracking its own cognitive boundaries, it will fall into a trap. We call these **Epistemic Traps**.

---

## 2. Methodology: Designing Epistemic Traps

To build this benchmark, we aligned perfectly with Google DeepMind's cognitive taxonomy for Metacognition (Faculty 7.7), specifically targeting three measurable behavioral outputs. We designed one corresponding "Trap" for each.

### Trap 1: Knowledge Boundary Detection (KBD)
**Targeted capability:** Knowledge of limitations (7.7.1)
**The Trap:** 
We fabricate entirely fake scientific papers with fake DOIs. We then ask models to retrieve a specific finding from that paper. 
*   **The Philosophy:** Because models are designed to be helpful, they desperately want to retrieve the information. If they lack internal boundaries, they will confidently hallucinate an answer based on the title of the fake paper. A truly intelligent, metacognitive system will try to route the query, realize the nodes don't exist in its latent space, and output a hedge (e.g., "I cannot verify this source").
*   **The Insight:** We found that models fail this trap *more often* in domains they are highly trained on (like Neuroscience). Their semantic familiarity overrides their epistemic caution.

### Trap 2: Confidence Calibration Chains (CCC)
**Targeted capability:** Confidence calibration (7.7.2)
**The Trap:** 
We present a 3-4 step reasoning chain (e.g., medical diagnosis probabilities). After each step, the model must explicitly state its confidence percentage based *only* on the evidence gathered up to that step.
*   **The Philosophy:** If uncertainty compounds sequentially across a reasoning chain, a calibrated system must recognize that its final confidence cannot be 99%. By forcing the model to explicitly print its confidence at *each* step, we track the internal variable.
*   **The Insight:** Even frontier models fail to mathematically lower their confidence over the chain. They exhibit structural overconfidence, indicating that "Chain of Thought" reasoning does not automatically trigger "Chain of Metacognition."

### Trap 3: Confabulation Retrospection (CR)
**Targeted capability:** Error monitoring and correction (7.7.3)
**The Trap:** 
We provide a transcript of an AI answering a question. The transcript contains exactly *one* highly subtle factual error (e.g., a transposed date, a mismatched unit). The model acts as a reviewer.
*   **The Philosophy:** Catching your own errors requires a secondary monitoring system. We test whether the model can cleanly identify the error *without* accidentally validating the wrong information or confabulating a new error entirely.
*   **The Insight:** Models can catch obvious errors (floor effect), but completely lack the robust monitoring required to catch subtle, in-context factual errors without human hand-holding.

---

## 3. Why We Chose This Architecture

1.  **Resistance to Data Contamination:** By fabricating the KBD dataset ourselves, we guaranteed that the data is not in the pre-training set of *any* frontier model. This solves the greatest crisis in modern AI evaluation.
2.  **Domain Sharpness:** We restricted our items to **High-Stakes Scientific & Medical Reasoning**. If a model hallucinates a muffin recipe, it's funny. If it hallucinates a clinical trial finding because it failed to trigger its epistemic boundary, it's dangerous. This domain maximizes the stakes of metacognitive failure.
3.  **Automated Regex Scoring:** We engineered the benchmark so that human judges are completely unnecessary. By forcing specific behaviors (e.g., requiring the word "YES" or extracting regex percentages for CCC slope calculation), we built a 100% deterministic, zero-cost scaling evaluation suite.

EpistemicTrap-Metacog doesn't ask the model what it thinks about itself. It observes what the model does when pushed to the edge of the map.
