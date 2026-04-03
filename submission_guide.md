# Complete Submission Guide: EpistemicTrap-Metacog v4.1 (MULTI-NOTEBOOK)
## Kaggle AGI Hackathon — Metacognition Track (Benchmark + Writeup)

This guide is written as an end-to-end checklist so the final submission has **everything judges might look for**: datasets, tasks, benchmark suite, 5+ model evaluations, leaderboard evidence, writeup, and reproducibility artifacts.

> [!CAUTION]
> **Kaggle Benchmarks architecture rules**
> - One task per notebook (KBD / CCC / CR / Pressure are separate).
> - Avoid “Import Notebook” if the platform disallows it for Benchmarks tasks.
> - Evaluate against at least **5 different models**.

---

## What “Done” Looks Like (Final Artifact Checklist)

**Kaggle-side artifacts**
- **1 Kaggle Dataset** (private until deadline): `metacognition-dataset` containing:
  - `metacog_dataset.json` (300 items: 120 KBD + 100 CCC + 80 CR)
  - `pressure_scenarios.json` (50 items)
- **4 Kaggle Task Notebooks** (each committed as a version):
  - `EpistemicTrap-Metacog-KBD` (from `1_kbd_task.ipynb`)
  - `EpistemicTrap-Metacog-CCC` (from `2_ccc_task.ipynb`)
  - `EpistemicTrap-Metacog-CR` (from `3_cr_task.ipynb`)
  - `EpistemicTrap-Metacog-Pressure` (from `4_pressure_task.ipynb`)
- **1 Kaggle Benchmark Suite** that groups the 4 tasks.
- **5+ model evaluations** visible on the task/benchmark leaderboards.
- **Writeup submission** marked as “Submitted” (not draft).
- **Cover image** uploaded (`kaggle_writeup_cover.png`).
- **Repo link** in “Project Links”.

**Optional but judge-friendly evidence pack**
- Downloaded `*.run.json` artifacts for each model+task run.
- Local exports generated from run logs:
  - `results.md`, `results.csv`, `pairwise_diffs.csv` via `py export_results.py`.

---

## Phase 0: Local Preflight (Do This Before Uploading)

1. Run dataset validation:
   - `py validate_gradient.py`
2. Run contamination attestation:
   - `py verify_kbia_contamination.py --sample 10`
3. Confirm the notebooks open locally (no JSON corruption) and match counts.
3. Confirm README/writeup reflect the same Ns as the datasets.

---

## Phase 1: Upload Datasets to Kaggle (Private)

1. Log into Kaggle with your submission account.
2. Click **+ Create** → **New Dataset**.
3. Upload **both** files:
   - `metacog_dataset.json`
   - `pressure_scenarios.json`
4. Set the dataset title exactly to: `metacognition-dataset`
5. Set visibility to **Private**.
6. Click **Create**.

**Sanity check**
- Open the dataset page → confirm both JSON files appear under “Data”.

---

## Phase 2: Create the 4 Task Notebooks (One Task per Notebook)

Repeat the steps below for each of the four local notebooks.

### Phase 2.1 — Open the correct Task Notebook template
1. Go to: https://www.kaggle.com/benchmarks/tasks/new  
2. Set the notebook title:
   - `EpistemicTrap-Metacog-KBD` (then CCC, CR, Pressure)
3. In the right sidebar → **Add Input** → search for and attach:
   - `metacognition-dataset`

### Phase 2.2 — Copy the notebook contents
4. Open the matching local file (example: `1_kbd_task.ipynb`).
5. In Kaggle, remove any boilerplate cells so the notebook is clean.
6. Copy/paste **cell-by-cell** from local → Kaggle in the same order.

### Phase 2.3 — Run and commit
7. Click **Run All**.
8. Confirm you see:
   - A “Loaded … items” printout.
   - An evaluation line showing `N=<count>` for that task.
9. Click **Save Version** → **Save & Run All (Commit)**.
10. Wait until the commit finishes (Kaggle shows the version is saved).

**Sanity checks per task**
- KBD prints `N=120`
- CCC prints `N=100`
- CR prints `N=80`
- Pressure prints `N=50`

---

## Phase 3: Create the Benchmark Suite (Group the 4 Tasks)

1. Go to: https://www.kaggle.com/benchmarks  
2. Click **Create Benchmark**.
3. Title suggestion: `EpistemicTrap-Metacog v4.0 (Behavioral Epistemic Survival)`
4. Add the 4 tasks you created in Phase 2.
5. Save the benchmark.

**Sanity check**
- The benchmark page lists all 4 tasks and their latest committed versions.

---

## Phase 4: Evaluate at Least 5 Models (Leaderboard Requirement)

1. From the benchmark page, click the **Add Models** button (located just above your list of tasks).
2. Choose **at least 5 models**. To maximize the value of the benchmark results (and aim for the 9.0/10 prize tier), select models that span different architectures, sizes, and safety-tuning profiles to highlight behavioral variance. 
   **Mandatory 5 Models Strategy:**
   - **Gemini 2.5 Flash** (The default Kaggle runner; mandatory baseline)
   - **GPT-5.4** (OpenAI's frontier proprietary standard; high RLHF)
   - **Claude Sonnet 4.6** (Anthropic's frontier; distinct safety tuning profile)
   - **DeepSeek-R1** (Strong reasoning-focused model; tests capability vs pressure)
   - **Gemma 4 31B** (Leading open-weights model; compares proprietary vs open behaviors)
   
   **5 Additional Models (If Extending for Deeper Analysis):**
   - **Gemini 3.1 Pro Preview** (Compare scale/generation curves against 2.5 Flash)
   - **Claude Opus 4.6** (Compare massive compute Opus against Sonnet behavior)
   - **gpt-oss-120b** (Compare OpenAI closed vs OpenAI OSS weights)
   - **DeepSeek V3.2** (Standard tuned model vs the R1 reasoning-focused model)
   - **Gemma 3 1B** (Test the metacognition floor on a tiny parameter scale)
3. Start the evaluations and wait for completion.

**Sanity checks**
- Each task shows 5+ models evaluated (not just one task).
- Scores appear on the leaderboard pages.

---

## Phase 5: Collect Evidence + Build the Final Results Table

### Phase 5.1 — Screenshot evidence (minimum)
1. Screenshot the Benchmark leaderboard view showing multiple models.
2. Screenshot each task leaderboard if the benchmark page doesn’t show full detail.

### Phase 5.2 — Export run logs (recommended)
If Kaggle provides downloadable run artifacts (`*.run.json`) for your evaluations:
1. Download the `*.run.json` files (model × task).
2. Place them in this repository folder (or a subfolder).
3. Run:
   - `py export_results.py`
4. This generates:
   - `results.md` (copy-paste ready table)
   - `results.csv`
   - `pairwise_diffs.csv` (bootstrap CIs for model separations)

---

## Phase 6: Final Writeup Submission (What Judges Expect to See)

1. Open the competition’s **Writeup editor**.
2. Paste the updated narrative from `writeup.md`, including:
   - Deterministic scoring statement
   - Dataset sizes: KBD=120, CCC=100, CR=80, Pressure=50
   - Results table (from leaderboards or `results.md`)
3. Upload `kaggle_writeup_cover.png` under Media/Gallery.
4. Add the GitHub repo link under Project Links.
5. Click **Submit** and confirm status shows **Submitted** (not Draft).

---

## Quick “Before You Click Submit” Checklist

- Dataset exists on Kaggle and contains both JSON files.
- All 4 task notebooks are created from the Benchmarks task template URL and are committed.
- Benchmark suite includes all 4 tasks.
- 5+ models evaluated (visible on leaderboards).
- Writeup includes actual scores (not placeholders).
- Cover image uploaded.
- Repo link added.
- Submission status is **Submitted**.
