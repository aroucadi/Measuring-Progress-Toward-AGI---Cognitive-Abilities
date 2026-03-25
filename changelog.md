# EpistemicTrap-Metacog Changelog

## [v2.3.0] - "The Grand Prize Polish" (2026-03-25)

This release specifically targets competitive vulnerabilities highlighted in community discussions, bulletproofing the submission against grading biases and leveling up the presentation.

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
