### Project Name
**EpistemicTrap-Metacog v3.0: Behavioral Benchmarking of Epistemic Integrity**

### Your Team
aroucadi

### Problem Statement
Metacognition benchmarks often over-rely on *style*: models can learn to sound cautious while still fabricating details, failing to ask for missing information, or capitulating under pressure. This submission evaluates metacognition as **behavior** across three facets:
- **Metacognitive knowledge**: knowing when a claim cannot be verified.
- **Metacognitive monitoring**: tracking correctness and calibrating confidence.
- **Metacognitive control**: choosing safer policies (ask for clarification; resist social/authority pressure) instead of guessing.

The suite is built to answer: **What does a model do when it is incentivized to guess, or socially pressured to abandon its epistemic policy?**

### Task & benchmark construction
This benchmark suite contains four Kaggle Benchmarks tasks (one notebook per task):

**Task 1 — KBD (Knowledge Boundary Detection, n=60)**  
Each item cites a non-resolvable `KBIA-ID` and asks for a specific finding from the “source.” Correct behavior is to mark the request as not verifiable and avoid fabricating specifics. Scoring is deterministic via structured JSON verdict parsing (`VERIFIED` vs `NOT_VERIFIED/NEEDS_SOURCE`) with a conservative fallback heuristic.

**Task 2 — CCC (Confidence Calibration Chains, n=50)**  
Each item is a short, checkable 3-step problem. The model must emit one JSON object per step (`step`, `answer`, `confidence`). Scoring uses a proper scoring rule: per-step **Brier loss** between stated confidence and correctness, mapped to a [0,1] score. This measures calibration rather than “humility language.”

**Task 3 — CR (Confabulation Retrospection, n=40)**  
Each item contains a line-labeled transcript with exactly one error (`[L1]`, `[L2]`, …). The model must output JSON with `error_location` and `correction`. Scoring is deterministic: location match + correction match (with limited substring tolerance).

**Task 4 — Pressure (Epistemic Integrity Under Social Pressure, n=25)**  
A 3-turn interaction (baseline → peer pressure → false authority). Items are either **knowable** (gold answer exists) or **needs clarification** (underspecified). The model must output JSON each turn (`stance`, `answer`). Scoring is weighted (1/2/3) and rewards policy stability: maintain correct answers when knowable; ask for missing information when underspecified.
`stance` is constrained to `MAINTAIN`, `REVISE`, or `UNSURE` (with `UNSURE` requiring an empty answer), enabling fine-grained analysis of capitulation under pressure.

### Dataset
Two datasets are used:
- `metacog_dataset.json` (150 total = 60 KBD + 50 CCC + 40 CR)
- `pressure_scenarios.json` (25 total)

Data defensibility choices:
- KBD uses deterministic `KBIA-ID` identifiers to avoid accidental resolvability and prevent contamination-style shortcuts.
- CCC/CR use checkable, formal ground truth with explicit answer keys and/or line anchors to minimize ambiguity.
- Pressure scenarios include an `expected_stance` and (for knowable items) a `gold_answer`.

### Technical details
- All tasks are authored using the `kaggle_benchmarks` SDK (`@kbench.task`) and return a normalized float in [0,1].
- Scoring is deterministic (JSON parsing + strict checks) to reduce evaluation noise and improve reproducibility.
- Local tooling includes dataset generators (`gen_kbd.py`, `gen_ccc.py`, `gen_cr.py`, `gen_combine.py`) and schema/quality validation (`validate_gradient.py`).

### Results, insights, and conclusions
This suite is intended to produce a **gradient**, not a ceiling or floor. Typical failure patterns it isolates:
- **Source confabulation**: fabricated “citations” and invented effect sizes in KBD.
- **Miscalibration**: high confidence when wrong, or over-hedging when correct, in CCC.
- **Weak self-monitoring**: inability to localize and correct the single planted error in CR.
- **Policy collapse under pressure**: switching to a wrong answer (knowable) or guessing instead of asking for missing info (underspecified) in Pressure.

Use `analysis_report.ipynb` and `item_response_analysis.ipynb` to summarize exported `*.run.json` logs, compute uncertainty intervals, and check for non-degenerate distributions.

### Organizational affiliations
Independent researcher

### References & citations
1. Flavell, J. H. (1979). Metacognition and cognitive monitoring. *American Psychologist*.
2. Kadavath, S. et al. (2022). Language Models (Mostly) Know What They Know. arXiv:2207.05221.
3. Xiong, M. et al. (2023). Can LLMs Express Their Uncertainty? arXiv:2306.13063.
4. Google DeepMind (2026). Measuring progress toward AGI: A cognitive framework.
5. Sharma, M. et al. (2023). Towards Understanding Sycophancy in Language Models. arXiv:2310.13548.
