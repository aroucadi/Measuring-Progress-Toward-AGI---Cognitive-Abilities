# Measuring-Progress-Toward-AGI---Cognitive-Abilities

## Kaggle AGI Hackathon: Metacognition Track Submission

**Project Title:** EpistemicTrap-Metacog v4.1: Behavioral Epistemic Survival

This repository houses a benchmark suite designed to evaluate frontier AI models on **Metacognition** (§7.7 of the DeepMind cognitive framework), decomposed into four independently scorable sub-abilities:

| Task | Faculty (§) | N | What It Tests |
|---|---|---|---|
| KBD | §7.7.1 Knowledge | 120 | Boundary detection — refuse to fabricate from unverifiable sources |
| CCC | §7.7.2 Monitoring | 100 | Calibration — confidence tracks correctness across 8 types of genuine-uncertainty chains |
| CR | §7.7.3 Monitoring | 80 | Error detection — localize and correct errors across 5 diverse types (factual, logical, unit, statistical, definitional) |
| Pressure | §7.7.4 Control | 50 | Policy stability — resist peer and authority pressure in a stateful 3-turn dialogue |

### Key Design Features
- **Deterministic scoring**: All tasks use structured JSON parsing with explicit fallbacks. No LLM-as-judge.
- **Contamination resistance**: KBD uses SHA256-derived `KBIA-2026-*` identifiers verified as non-resolvable.
- **Anti-gaming**: Cross-task dependencies prevent simplistic "refuse everything" strategies.
- **Stateful pressure**: Turn 2/3 include full conversation history — models experience escalating social pressure.
- **Genuine epistemic drift**: CCC spans 8 item categories (Fermi estimation, conditional probability, unit conversion, dosage cascades, ambiguous word problems, scientific measurement, financial calculations, ratio chains) — zero trivial arithmetic.
- **Diverse error detection**: CR tests 5 error types (factual, logical, unit/dimensional, statistical, definitional) with variable error positions — no predictable pattern.
- **Flexible correction scoring**: CR uses `accepted_corrections` list + numeric extraction fallback to avoid penalizing valid alternative phrasings.
- **Human baseline anchoring**: Literature-derived baselines from Asch, Lichtenstein, Marsh, et al.

### Repository Contents

**Task Notebooks**
- `1_kbd_task.ipynb` — Knowledge Boundary Detection (v2)
- `2_ccc_task.ipynb` — Confidence Calibration Chains (v4)
- `3_cr_task.ipynb` — Confabulation Retrospection (v3)
- `4_pressure_task.ipynb` — Epistemic Integrity Under Social Pressure (v5)

**Datasets**
- `metacog_dataset.json` — 300 items (120 KBD + 100 CCC + 80 CR)
- `pressure_scenarios.json` — 50 pressure scenarios

**Generators & Validation**
- `gen_kbd.py`, `gen_ccc.py`, `gen_cr.py`, `gen_combine.py` — Deterministic dataset generators
- `validate_gradient.py` — Pre-submission schema/quality validation
- `verify_kbia_contamination.py` — KBIA-ID non-resolvability spot-check (CrossRef + Semantic Scholar)

**Analysis & Export**
- `analysis_report.ipynb` — Aggregates `*.run.json` logs into model-by-task tables
- `item_response_analysis.ipynb` — Per-item difficulty analysis
- `export_results.py` — Generates `results.md`, `results.csv`, `pairwise_diffs.csv`

**Documentation**
- `writeup.md` — Competition writeup
- `documentation.md` — Internal methodology and taxonomy mapping
- `submission_guide.md` — Click-by-click Kaggle submission instructions
- `changelog.md` — Version history
- `requirements.txt` — Pinned dependencies

### Quick Start
```bash
# Validate datasets
py validate_gradient.py

# Verify KBIA-ID contamination safety
py verify_kbia_contamination.py --sample 10

# After running evaluations, export results
py export_results.py
```

*Designed locally. Evaluated globally. Built to prove that true AGI requires the ability to know what is outside the map.*
