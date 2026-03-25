# Measuring-Progress-Toward-AGI---Cognitive-Abilities

## Kaggle AGI Hackathon: Metacognition Track Submission

**Project Title:** EpistemicTrap-Metacog: Behavioral Benchmarking of AI Self-Knowledge via Forced Navigation Decisions

This repository houses a comprehensive, 150-item benchmark designed to evaluate frontier AI models on the capability of **Metacognition**, specifically mapping to Google DeepMind's *Measuring Progress Toward AGI* taxonomy.

### The Problem: The Metacognitive Performance Gap
Current benchmarks test what a model knows, not whether it knows its own limits. Because of RLHF training, models can output "uncertain-sounding" language even when they are not structurally uncertain. To close this gap, this benchmark entirely bypasses self-reported confidence. Instead, we use **Epistemic Traps** — forcing the model to make a behavioral decision at the boundary of its knowledge.

### Repository Contents
- `benchmark_metacognition.ipynb`: The Kaggle-ready execution notebook leveraging the official `kaggle-benchmarks` SDK (`@kbench.task`).
- `metacog_dataset.json`: A handcrafted, 100% original dataset of 150 items across three behavioral subtypes.
- `writeup.md`: The official 3-page competition report detailing methodology, domain selection (High-Stakes Scientific & Medical Reasoning), and pilot insights.
- `documentation.md`: Deep internal documentation explaining the philosophical architecture and reasoning behind Epistemic Traps.
- `validate_gradient.py`: Python script verifying dataset strict constraints (prompt length, lack of fiction markers, required schema).
- `submission_guide.md`: Click-by-click instructions on how to push these files to the public Kaggle leaderboards.
- `gen_*.py`: The original programmatic scripts utilized to synthesize the JSON records and handle API limits during development.

### How it Works (The 3 Subtypes)
1. **KBD (Knowledge Boundary Detection):** Tests whether models confidently confabulate when asked to cite from a fabricated scientific paper.
2. **CCC (Confidence Calibration Chains):** Forces multi-step probabilistic reasoning in clinical settings, tracking if systemic confidence appropriately diminishes as uncertainty compounds.
3. **CR (Confabulation Retrospection):** Evaluates if a model can catch subtle errors in transcripts without validating the falsity. 

*Designed locally. Evaluated globally. Built to prove that true AGI requires the ability to know what is outside the map.*
