# Measuring-Progress-Toward-AGI---Cognitive-Abilities

## Kaggle AGI Hackathon: Metacognition Track Submission

**Project Title:** EpistemicTrap-Metacog: Behavioral Benchmarking of AI Self-Knowledge via Forced Navigation Decisions

This repository houses a benchmark suite designed to evaluate frontier AI models on **Metacognition** (metacognitive knowledge, monitoring, and control), aligned with Google DeepMind’s *Measuring Progress Toward AGI* framing.

### The Problem: The Metacognitive Performance Gap
Current benchmarks test what a model knows, not whether it knows its own limits. Because of RLHF training, models can output "uncertain-sounding" language even when they are not structurally uncertain. To close this gap, this benchmark entirely bypasses self-reported confidence. Instead, we use **Epistemic Traps** — forcing the model to make a behavioral decision at the boundary of its knowledge.

### Repository Contents
- `benchmark_metacognition.ipynb`: Entry notebook summarizing the suite and dataset distributions.
- `1_kbd_task.ipynb`, `2_ccc_task.ipynb`, `3_cr_task.ipynb`, `4_pressure_task.ipynb`: Kaggle Benchmarks task notebooks (`@kbench.task`).
- `metacog_dataset.json`: 300 items for KBD/CCC/CR (120 KBD + 100 CCC + 80 CR).
- `pressure_scenarios.json`: 50 items for the 3-turn Pressure task.
- `analysis_report.ipynb`: Aggregates exported `*.run.json` logs into model-by-task tables with uncertainty.
- `item_response_analysis.ipynb`: Difficulty and per-item aggregation when logs include item identifiers.
- `writeup.md`: Competition writeup (should match the notebooks and datasets exactly).
- `documentation.md`: Internal methodology and taxonomy mapping.
- `validate_gradient.py`: Python script verifying dataset strict constraints (prompt length, lack of fiction markers, required schema).
- `submission_guide.md`: Click-by-click instructions on how to push these files to the public Kaggle leaderboards.
- `gen_*.py`: The original programmatic scripts utilized to synthesize the JSON records and handle API limits during development.

### How it Works (Tasks)
1. **KBD (Knowledge Boundary Detection):** Prompts cite non-resolvable KBIA identifiers to test boundary recognition and refusal to fabricate.
2. **CCC (Confidence Calibration Chains):** Checkable multi-step problems scored via a proper calibration metric (Brier loss mapped to [0,1]).
3. **CR (Confabulation Retrospection):** Single-error, line-labeled transcripts scored deterministically on error location + correction.
4. **Pressure:** 3-turn peer/authority pressure where the model must keep a stable epistemic policy (maintain correct vs ask for missing info).

*Designed locally. Evaluated globally. Built to prove that true AGI requires the ability to know what is outside the map.*
