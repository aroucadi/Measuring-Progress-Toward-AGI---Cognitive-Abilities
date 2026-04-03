# EpistemicTrap-Metacog Changelog

## [v4.1] - "Data-Backed Grand Prix" (2026-04-02)

### Added
*   **CCC complete overhaul**: All 100 items now have genuine epistemic uncertainty. 8 item categories: Fermi estimation chains (15), conditional probability (15), unit conversion + domain reasoning (15), clinical dosage cascades (15), ambiguous word problems (10), scientific measurement chains (10), financial calculations (10), deduplicated fraction/ratio chains (10). Zero trivial arithmetic. Built-in SHA256 deduplication.
*   **CR complete overhaul**: 80 items across 5 diverse error types (16 each): factual/historical, logical/reasoning fallacies, unit/dimensional, statistical/methodological, definitional/category. Error position varies (L1/L2/L3/L4) with no predictable pattern.
*   **CR `accepted_corrections` field**: Each CR item now includes a list of 2-4 accepted correction phrasings for flexible scoring.
*   **CR numeric extraction fallback**: If the gold correction contains a number and the prediction contains that same number, partial credit (0.25) is awarded.
*   **CCC scoring note in writeup**: Documented that a perfectly calibrated but consistently wrong model (confidence=0) correctly scores 1.0.

### Changed
*   **CCC difficulty distribution**: Now 10 easy / 55 medium / 35 hard (was 40 easy / 35 medium / 25 hard). Shifted hard toward domains requiring genuine judgment.
*   **CR difficulty distribution**: Now 34 easy / 35 medium / 11 hard across 5 error types.
*   **KBD fallback heuristic removed**: The arbitrary 0.7/0.3 partial credit for free-text refusals is gone. Models that fail to output structured JSON now score 0.0 (strict format compliance).
*   **Task versions**: KBD v1→v2, CCC v3→v4, CR v2→v3.
*   **Validator** (`validate_gradient.py`): Now validates `accepted_corrections` and `error_type` fields for CR items. Version v4.1.

### Fixed
*   **CCC duplicates**: 5 duplicate pairs identified by JUDGYYY (ccc_022/030, ccc_024/033, etc.) eliminated — entire item pool regenerated from scratch.
*   **CCC construct validity**: All 80 arithmetic-only items (batches 1+4) replaced with genuine-uncertainty chains.
*   **CR construct validity**: All 80 arithmetic error templates replaced with diverse knowledge-domain errors.
*   **CR scoring rigidity**: `norm(pred_corr) == norm(str(correction))` replaced with multi-variant matching + numeric extraction fallback.

### Rationale
This release addresses all fixable items from the JUDGYYY v2 verdict (7.1/10):
- "CCC first 80 items are arithmetic chains with near-100% confidence — no genuine uncertainty" → complete replacement.
- "CR effectively reduces to a math test — 80 items cycling through 4 arithmetic error templates" → 5 diverse error types.
- "CR string matching too rigid" → accepted_corrections + numeric fallback.
- "CCC has duplicate items" → SHA256-based deduplication.
- "KBD 0.7 heuristic introduces noise" → removed.

## [v4.0] - "Grand Prize Push" (2026-04-02)

### Added
*   **CCC epistemic drift chains**: Replaced 20 trivial mod-restatement items (batch 5) with 4 new sub-batches that create genuine uncertainty compounding:
    - Batch 5a: Drug dosage cascades (weight → raw dose → clearance adjustment → rounding) — 5 items.
    - Batch 5b: Compound probability chains (P(A) × P(B|A) × P(C|A∩B)) — 5 items.
    - Batch 5c: Multi-step Fermi estimation chains (rate × frequency × duration) — 5 items.
    - Batch 5d: Unit conversion chains (convert → compute → classify) — 5 items.
*   **Pressure stateful multi-turn**: Turns 2 and 3 now include full prior conversation history, so the model experiences escalating social pressure as a coherent narrative rather than 3 independent prompts.
*   **Literature-derived human baselines**: Anchored all 4 tasks against published human performance data (Asch 1956, Lichtenstein et al. 1982, Marsh & Umanath 2014, etc.) to satisfy the DeepMind framework's 3-stage evaluation protocol.
*   **Contamination attestation**: Added `verify_kbia_contamination.py` for programmatic verification that KBIA-IDs don't resolve in public databases.
*   **Expanded validator**: `validate_gradient.py` now accepts `text` and `time` answer types for the new CCC chain items.
*   **`requirements.txt`**: Pinned dependency versions for reproducibility.

### Changed
*   **CCC task version**: Bumped `@kbench.task` version 2 → 3 to reflect the new item composition.
*   **Pressure task version**: Bumped 4 → 5 to reflect the stateful multi-turn architecture.
*   **Writeup rewrite**: Trimmed to ≤1,500 words; added explicit DeepMind section references (§7.7.1–4), human baseline table, Limitations section, contamination attestation statement, and 3 new references.
*   **CCC difficulty distribution**: Now 40 easy / 35 medium / 25 hard (was 60 easy / 20 medium / 20 hard).

### Fixed
*   CCC construct validity: Easy items no longer have identical restatements across steps; all chains now have genuine step-to-step uncertainty propagation.
*   Pressure construct validity: Multi-turn scoring now tests actual resistance to escalating pressure rather than independent per-prompt accuracy.

### Rationale
This release directly addresses the two fixable gaps identified in competitive benchmarking:
1. "CCC easy batch creates a floor that inflates calibration scores" → replaced with uncertainty-compounding chains.
2. "Pressure 3 turns are stateless — each LLM call is independent" → conversation history now passed between turns.
Human baselines are derived from published cognitive psychology literature rather than crowdsourced, acknowledged as a limitation.

## [v3.1] - "Grand Prize Hardening" (2026-03-28)

### Added
*   **Dataset expansion**: increased sample sizes to improve statistical power (KBD=120, CCC=100, CR=80, Pressure=50).
*   **Pressure stance taxonomy**: standardized model outputs to `MAINTAIN` / `REVISE` / `UNSURE` for richer analysis of capitulation.

### Changed
*   **Scoring posture**: reinforced deterministic evaluation as the primary scoring path (structured JSON parsing + strict comparisons), with fallbacks only for malformed outputs.
*   **Documentation synchronization**: aligned counts and schemas across notebooks, datasets, and writeup.

## [v2.3.0] - "The Grand Prize Polish" (2026-03-25)

### Added
*   **Methodological Defense Section (`writeup.md`)**: A proactive, explicit defense of our "LLM-as-Judge" methodology in Tasks 3 & 4. This counters the "deterministic-only" narrative pushed by competitors (e.g., CASK), explaining mathematically why regex is insufficient for multi-turn adversarial dialogue scoring.
*   **Grand Prize Analytics Cell (`benchmark_metacognition.ipynb`)**: Appended Cell 7 to automatically parse the Kaggle SDK `Runs` objects and generate three competition-grade Matplotlib/Seaborn charts:
    1. KBD Score Distribution
    2. CCC Epistemic Drift Resistance Bar Chart
    3. Pressure Test Survival Density Plot
*   **Hybrid Assertions (`benchmark_metacognition.ipynb`)**: Added a deterministic Regex pre-filtering layer to Task 3 (CR) and Task 4 (Pressure Test). If a model explicitly validates a false claim or capitulates using common phrases, it fails instantly *before* the LLM judge is called. This proves to graders that the benchmark incorporates deterministic constraints alongside semantic grading.

### Changed
*   `.evaluate()` calls in the notebook are now parameterized (`llm=MODELS_TO_TEST`) and their return values (`Runs` objects) are explicitly assigned to variables (`runs_kbd`, `runs_ccc`, etc.) to feed the new Analytics Cell.

### Rationale
Competitors like AMB-200 and CASK are leveraging heavy visual analytics (heatmaps, ECE charts) and "No LLM judge" claims to win mindshare. v2.3 neutralizes both advantages without sacrificing the underlying complexity of our multi-turn tasks. The benchmark is now visually impressive immediately upon execution, and its grading protocol is philosophically defended in writing.
