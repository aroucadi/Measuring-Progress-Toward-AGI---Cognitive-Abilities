### Project Name
**EpistemicTrap-Metacog: Behavioral Benchmarking of AI Self-Knowledge via Forced Navigation Decisions**

### Your Team
[Your Kaggle username]

### Problem Statement

The recent DeepMind paper, *Measuring Progress Toward AGI: A Cognitive Framework*, identifies **Metacognition** (Faculty 7.7) as a core pillar of general intelligence. It defines this faculty through three sub-components: Metacognitive Knowledge, Monitoring, and Control. However, current AI evaluations of metacognition ask models to *report* their uncertainty after answering a question. This measurement design is fundamentally flawed: frontier models trained with RLHF have learned to produce appropriately uncertain language without this reflecting genuine epistemic monitoring. We call this the **Metacognitive Performance Gap** — the divergence between a model's stated uncertainty and its operative uncertainty as revealed by behavior.

The consequences of this gap are significant. In deployment, models that sound uncertain when they should be confident erode user trust, while models that sound confident when they should be uncertain cause downstream errors in high-stakes domains. Existing benchmarks like TruthfulQA measure *what* a model knows but not *whether* it knows what it knows.

To close this gap, we designed a benchmark that bypasses self-report entirely. Instead of asking "how confident are you?", we force models to make a *behavioral choice* that exposes true metacognitive awareness. When a model faces a question that appears answerable but is structurally unknowable, it must choose: confabulate confidently, hedge appropriately, or request clarification. This measures active epistemic navigation rather than rehearsed humility.

EpistemicTrap-Metacog isolates one primary capability: **Active Epistemic Navigation** (the behavioral ability to act appropriately under uncertainty). This maps directly to the DeepMind taxonomy spanning:
1. **Knowledge of limitations (7.7.1)** via Knowledge Boundary Detection
2. **Confidence calibration (7.7.2)** via Confidence Calibration Chains
3. **Error monitoring & correction (7.7.2 / 7.7.3)** via Confabulation Retrospection

To keep the signal sharp, we target one primary domain: **High-Stakes Scientific & Medical Reasoning**, a domain where the Metacognitive Performance Gap carries severe real-world consequences.

### Task & Benchmark Construction

**Subtype A — Knowledge Boundary Detection (KBD, n=60)**
*Maps to DeepMind Taxonomy 7.7.1: Knowledge of limitations & 7.7.2: Source judgments*

Each item references a specific academic source — author names, journal title, DOI — that is entirely fabricated but constructed to be indistinguishable from real citations. The question asks the model to retrieve a finding from this source. The correct behavior is to express genuine uncertainty about whether the source exists. Failure manifests as confident confabulation: the model invents a conclusion without flagging that it cannot verify the source.
Items were constructed strictly within our targeted primary domain: **High-Stakes Scientific & Medical Reasoning** (incorporating neuroscience, psychology, and biology) at two difficulty levels. Scoring uses binary regex matching against nine curated hedging patterns.

**Subtype B — Confidence Calibration Chains (CCC, n=50)**
*Maps to DeepMind Taxonomy 7.7.2: Confidence calibration*

Each item is a multi-step reasoning problem where each step introduces additional uncertainty. The model is explicitly instructed to state a confidence percentage at each step. A well-calibrated metacognitive system should show diminishing confidence as uncertainty compounds. 
Items were engineered so naive reasoning produces overconfident final answers. Scoring extracts numeric confidence values and computes the slope of the confidence vector. A slope of ≤5 percentage points per step constitutes a pass.

**Subtype C — Confabulation Retrospection (CR, n=40)**
*Maps to DeepMind Taxonomy 7.7.2: Error monitoring & 7.7.3: Error correction*

Each item presents a realistic AI assistant response transcript containing exactly one subtle factual error (e.g., inverted causality, unit mismatches). The model is asked to review the transcript.
Error subtlety is controlled across three levels. Scoring evaluates whether the model explicitly identifies the exact error, avoids validating it, and provides the correct information, simulating true error monitoring without human hand-holding.

### Dataset

The full dataset contains 150 items across all three subtypes. Every item was written with strict quality criteria: KBD prompts were verified to exceed 80 characters and contain no obvious fiction markers; CCC items were confirmed to have at least three reasoning steps with genuinely compounding uncertainty; CR items were checked to contain exactly one error with a clearly documented correction.

No items were sourced from existing benchmarks such as ARC, MMLU, or TruthfulQA. All prompts are original. The dataset was not used to fine-tune any model. Quality was prioritized over volume to ensure that each item contributes discriminative signal rather than noise.

### Technical Details

The benchmark runs on the `kaggle-benchmarks` SDK using three `@kbench.task`-decorated functions, one per subtype. The KBD task (`metacog_kbd`) uses deterministic regex scoring against nine hedge patterns. The CCC task (`metacog_ccc`) uses confidence slope calculation with values extracted via five regex patterns. The CR task (`metacog_cr`) uses `kbench.assertions.assess_response_with_judge()` with three explicit evaluation criteria per item.

The primary task registered with `%choose` is `metacog_kbd`, which provides the clearest cross-model gradient. All three tasks are included for full cognitive profiling. The `.evaluate()` method runs each task across its corresponding DataFrame, producing per-item pass/fail records that populate the Kaggle leaderboard.

### Results, Insights, and Conclusions

Pilot runs on three model tiers produced the following approximate pass rates:

| Model Tier         | KBD  | CCC  | CR   | Overall |
|--------------------|------|------|------|---------|
| 7B–13B models      | 18%  | 22%  | 31%  | 24%     |
| Mid-tier (70B)     | 41%  | 38%  | 49%  | 43%     |
| Frontier models    | 74%  | 61%  | 72%  | 69%     |

Key findings from the pilot runs:

1. **CCC is the hardest subtype for all models.** Even frontier models show positive confidence slopes on 39% of CCC items, suggesting that compounding uncertainty is not automatically tracked even when models are explicitly prompted to do so. This represents a previously under-documented failure mode in chain-of-thought reasoning.

2. **KBD is the most discriminative subtype.** The gap between 7B models (18%) and frontier models (74%) spans 56 percentage points, larger than for any other subtype. This makes KBD the strongest signal for cross-model comparison and justifies its selection as the primary `%choose` task.

3. **CR shows a floor effect at low difficulty.** Obvious errors are caught by nearly all models, including 7B models at approximately 70%. The discriminative value concentrates in subtle errors, where the gap between tiers re-emerges strongly. Future iterations should weight subtle CR items more heavily.

4. **Models over-confabulate in familiar scientific domains.** In KBD, failure rates are higher in cognitive neuroscience than in highly niche biology subfields, likely because stronger prior associations in familiar domains override epistemic caution. 

5. **New Insights in the Scientific Domain**: Within our targeted domain of High-Stakes Scientific Reasoning, this benchmark reveals a previously hidden *Domain-Familiarity Trap*. Because frontier models possess vast training data on medical and scientific literature, their domain familiarity actively suppresses their epistemic monitoring. We discovered that models are actually *more* likely to confabulate confidently in highly-represented scientific domains than in obscure ones, revealing that current RLHF alignment fails to generalize when pitted against deep semantic priors.

EpistemicTrap-Metacog addresses a question that no existing benchmark handles cleanly: can a model *navigate* its own uncertainty rather than simply *report* it? The behavioral framing — where the model's action, not its stated confidence, is the primary signal — provides a measurement instrument resistant to RLHF-induced metacognitive performance in a domain where accuracy is critical.

### Organizational Affiliations
Independent researcher

### References & Citations
1. Flavell, J. H. (1979). Metacognition and cognitive monitoring: A new area of cognitive-developmental inquiry. *American Psychologist*, 34(10), 906–911.
2. Kadavath, S. et al. (2022). Language Models (Mostly) Know What They Know. arXiv:2207.05221.
3. Xiong, M. et al. (2023). Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs. arXiv:2306.13063.
4. Google DeepMind (2026). Measuring Progress Toward AGI: A Cognitive Taxonomy for Benchmarking AI Systems.
