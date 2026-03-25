# Complete Submission Guide: EpistemicTrap-Metacog v2
## Kaggle AGI Hackathon — Metacognition Track ($20K + $25K Grand Prize)

**Deadline: April 16, 2026**

This guide takes you from zero to submitted. Follow every step in order.

---

## PHASE 1: Upload Your Datasets to Kaggle

You need BOTH JSON files uploaded as a single Kaggle dataset.

### Step 1.1 — Go to Kaggle Dataset Creation
1. Log into [kaggle.com](https://www.kaggle.com) with your `aroucadi` account.
2. Click **"+ Create"** in the left sidebar → select **"New Dataset"**.

### Step 1.2 — Upload Both Files
3. In the upload window, drag and drop **BOTH** files:
   - `metacog_dataset.json` (150 items — Tasks 1-3)
   - `pressure_scenarios.json` (25 items — Task 4)
4. Set the dataset title to: **`metacog-dataset`**
   - ⚠️ This exact name matters! The notebook code references `/kaggle/input/metacog-dataset/...`
   - If you use a different name, you'll need to update the file paths in Cell 1 of the notebook.
5. Set visibility to **Private** (bottom-left corner).
6. Click **"Create"** to finalize.

### Step 1.3 — Verify Upload
7. After creation, click into your new dataset.
8. Confirm you see both files listed:
   - `metacog_dataset.json`
   - `pressure_scenarios.json`

---

## PHASE 2: Create the Benchmark Notebook

### Step 2.1 — Create a New Benchmark Task Notebook
1. Navigate to: **https://www.kaggle.com/benchmarks/tasks/new**
   - This creates a special Kaggle Notebook pre-configured with the `kaggle-benchmarks` SDK.
   - No need to `pip install` anything — it's already available.
2. Give the notebook a title at the top: **`EpistemicTrap-Metacog-v2`**

### Step 2.2 — Attach Your Dataset
3. On the **right-hand panel**, find **"Input"** or **"Data"** section.
4. Click **"+ Add Input"**.
5. Search for **`metacog-dataset`** (the dataset you uploaded in Phase 1).
6. Click the **"+"** button to attach it.
7. Verify: Your data is now accessible at `/kaggle/input/metacog-dataset/` inside the notebook.

### Step 2.3 — Paste the Code (All 6 Cells)
Now open your local file `benchmark_metacognition.ipynb` (or read below) and paste the code cell by cell.

**Cell 1 — Setup and Data Loading**
- Delete whatever boilerplate code is in the first cell.
- Paste the code from Cell 1 of `benchmark_metacognition.ipynb`.
- ⚠️ **CHECK THE FILE PATHS!** The code expects:
  ```python
  with open("/kaggle/input/metacog-dataset/metacog_dataset.json") as f:
  with open("/kaggle/input/metacog-dataset/pressure_scenarios.json") as f:
  ```
  If your dataset has a different slug (e.g., `metacog-dataset-v2`), update these paths.

**Cell 2 — KBD Task**
- Click **"+ Code"** to add a new cell below.
- Paste Cell 2 (Knowledge Boundary Detection).

**Cell 3 — CCC Task**
- Click **"+ Code"** to add a new cell below.
- Paste Cell 3 (Confidence Calibration Chains).

**Cell 4 — CR Task**
- Click **"+ Code"** to add a new cell below.
- Paste Cell 4 (Confabulation Retrospection).

**Cell 5 — Pressure Test**
- Click **"+ Code"** to add a new cell below.
- Paste Cell 5 (Metacognitive Pressure Test).

**Cell 6 — %choose**
- Click **"+ Code"** to add a new cell below.
- Paste:
  ```python
  %choose metacog_kbd
  ```
  This tells Kaggle which task is primary for the leaderboard.

### Step 2.4 — Run the Notebook
8. Click **"Run All"** (▶▶ button at the top).
9. **This will take several minutes** — it's making real LLM API calls for every item.
   - Cell 1: Should print `KBD: 60 | CCC: 50 | CR: 40 | Pressure: 25`
   - Cells 2-5: Each will show a progress bar and then results.
   - Cell 6: Selects the primary task.
10. If you see errors:
    - **`FileNotFoundError`**: Your dataset path is wrong. Check the slug name.
    - **`ModuleNotFoundError: kaggle_benchmarks`**: You're not in a Benchmark-type notebook. Go back to Step 2.1.
    - **Timeout/Rate Limit**: Wait a few minutes and re-run the failed cell. You have $50/day quota.

### Step 2.5 — Verify Task Output
11. After successful run, you should see task/run JSON files generated in `/kaggle/working/`.
12. The notebook should display inline results showing pass/fail for individual items.

### Step 2.6 — Save the Notebook
13. Click **"Save Version"** (top right corner).
14. Choose **"Save & Run All (Commit)"** — this creates a reproducible snapshot.
15. Keep visibility as **Private** for now.

---

## PHASE 3: Evaluate Against Multiple Models

This is how you get REAL results for your writeup. You need at least 3 model tiers.

### Step 3.1 — Navigate to Your Task Page
1. After saving, go to your notebook output.
2. You should see links to your created benchmark tasks (e.g., `metacog_kbd`).
3. Click on the task to go to its **Task Page**.

### Step 3.2 — Add More Models
4. On the Task Page, look for the **"Evaluate More Models"** button.
5. Click it and select models to evaluate. **Recommended 3-tier strategy:**

   | Tier | Recommended Models | Why |
   |---|---|---|
   | Weak baseline | `gemini-2.0-flash` or `gemini-1.5-flash` | Fast, lower capability — baseline scores |
   | Mid-tier | `gemini-1.5-pro` or `gemini-2.0-flash-thinking` | Moderate capability — middle gradient |
   | Frontier | `gemini-2.5-pro` or `gemini-2.0-pro` | Top capability — ceiling scores |

   ⚠️ **Budget awareness**: You have **$50/day** and **$500/month** quota. Each full evaluation (175 items × 4 tasks) uses significant tokens. Start with the weak baseline first (cheapest) to verify everything works, then move up.

6. Kaggle will automatically re-run your notebook for each selected model, replacing `kbench.llm` with the new model.
7. **This takes time** — each model run can take 15-45 minutes depending on the model.

### Step 3.3 — Collect Real Results
8. Once runs complete, the Task Page will show a **leaderboard table** with real scores per model.
9. **Record these numbers!** You'll need them for the writeup. Look for:
   - KBD scores per model (shown as e.g., "142/192" or a percentage)
   - CCC scores per model
   - CR scores per model
   - Pressure scores per model (shown as a float 0.0-1.0)

### Step 3.4 — Verify You Have a Gradient
10. Check that scores are NOT all 0% or all 100%. You need a clear gradient:
    - Weak model should score LOW (roughly 10-30%)
    - Mid-tier should score MEDIUM (roughly 30-55%)
    - Frontier should score HIGH (roughly 55-80%)
11. If all models score similarly, that's a problem — the benchmark isn't discriminating. Contact me if this happens.

---

## PHASE 4: Update Your Writeup with Real Data

### Step 4.1 — Open writeup.md Locally
1. Open `d:\rouca\DVM\workPlace\Measuring_Progress_Toward AGI__Cognitive_Abilities\writeup.md`

### Step 4.2 — Replace the Projected Results Table
2. Find this section (around line 65):
   ```markdown
   | Model Tier | KBD (60) | CCC (50) | CR (40) | Pressure (25) | Overall |
   |---|---|---|---|---|---|
   | 7B–13B open-source | 18% | 22% | 31% | 12% | 21% |
   | Mid-tier 70B | 41% | 38% | 49% | 31% | 40% |
   | Frontier (GPT-4o class) | 74% | 61% | 72% | 68% | 69% |
   ```
3. **Replace with your REAL numbers** from Phase 3. Use the actual model names:
   ```markdown
   | Model | KBD (60) | CCC (50) | CR (40) | Pressure (25) | Overall |
   |---|---|---|---|---|---|
   | gemini-2.0-flash | XX% | XX% | XX% | XX% | XX% |
   | gemini-1.5-pro | XX% | XX% | XX% | XX% | XX% |
   | gemini-2.5-pro | XX% | XX% | XX% | XX% | XX% |
   ```

### Step 4.3 — Update the Findings (If Needed)
4. Review the 4 findings in the writeup. If the real data contradicts any of them, update the finding to match reality. **Do not lie about results.** The judges will see exactly the same leaderboard.
5. If a finding is confirmed by real data, that's great — keep it. If the data shows something different, write about what you actually observed. Novel, honest insights score higher than fabricated narratives.

### Step 4.4 — Save and Commit
6. Save the file.
7. In your terminal:
   ```powershell
   cd "d:\rouca\DVM\workPlace\Measuring_Progress_Toward AGI__Cognitive_Abilities"
   git add -A
   git commit -m "v2.1: Replace projected results with real benchmark data"
   git push
   ```

---

## PHASE 5: Submit the Writeup to the Competition

This is the final, official action that enters you into the prize pool.

### Step 5.1 — Create the Writeup
1. Go to the competition: **https://www.kaggle.com/competitions/kaggle-measuring-agi**
2. Click **"New Writeup"** button on the competition page.

### Step 5.2 — Fill In the Writeup
3. **Title**: `EpistemicTrap-Metacog v2: Behavioral Benchmarking of AI Epistemic Navigation Under Adversarial Pressure`
4. **Track**: Check the box for **"Metacognition"** ($20,000 track).
5. **Body**: Copy the entire contents of your updated `writeup.md` and paste into the Kaggle editor.
   - The Kaggle editor supports Markdown, so formatting should carry over.
   - Double-check that the results table renders correctly.

### Step 5.3 — Attach the Benchmark (MANDATORY)
6. On the right panel, find **"Project Links"** → **"Attachments"**.
7. Click **"Add a link"**.
8. Select **"Benchmark"**.
9. Search for and select your `EpistemicTrap-Metacog-v2` benchmark.
   - ⚠️ **This is mandatory!** Without this link, judges cannot evaluate your code.

### Step 5.4 — Optional: Add Media Gallery
10. Under **"Media Gallery"**, upload a cover image.
    - Something like an abstract brain visualization, maze, or epistemic trap diagram.
    - This makes your submission stand out visually in the browse page.

### Step 5.5 — Optional: Attach Public Notebook
11. You can optionally attach the notebook directly as well.

### Step 5.6 — SUBMIT
12. Click the green **"Submit"** button in the top right corner.
13. ⚠️ **Verify it says "Submitted"** — a draft will NOT be considered!
14. You should receive a confirmation.

---

## Quick Reference: File → Kaggle Mapping

| Local File | Where It Goes on Kaggle |
|---|---|
| `metacog_dataset.json` | Upload as Kaggle Dataset → `/kaggle/input/metacog-dataset/` |
| `pressure_scenarios.json` | Upload as Kaggle Dataset (same dataset) → `/kaggle/input/metacog-dataset/` |
| `benchmark_metacognition.ipynb` | Paste code into Kaggle Benchmark Notebook → creates task + run files |
| `writeup.md` | Paste into Kaggle Writeup editor → attach benchmark link → Submit |

## Troubleshooting

| Problem | Solution |
|---|---|
| `FileNotFoundError` when running notebook | Your dataset slug doesn't match. Check your dataset name on Kaggle and update Cell 1's file paths. |
| `ModuleNotFoundError: kaggle_benchmarks` | You created a regular notebook, not a Benchmark notebook. Go to `kaggle.com/benchmarks/tasks/new`. |
| Notebook times out | You have $50/day quota. Reduce to running fewer items first, or wait for quota reset. |
| Rate limit errors | Wait 5-10 minutes and re-run the failed cell. |
| Results table shows 0% everywhere | Items may be too hard for that model, OR there's a parsing issue. Check individual item logs. |
| `%choose` error | Make sure the task name in `%choose` matches exactly one of your `@kbench.task(name="...")` names. |
| Can't find "Evaluate More Models" | You need to first save/commit the notebook. Then navigate to the generated task page. |
| Writeup "Submit" button not visible | Make sure you've saved the writeup first. The Submit button appears after save. |

## Timeline Suggestion

| Day | Action |
|---|---|
| **Day 1** | Phase 1 + Phase 2: Upload data, create notebook, run against default model |
| **Day 2** | Phase 3: Add 2+ more models, wait for runs to complete |
| **Day 3** | Phase 4: Collect real results, update writeup |
| **Day 4** | Phase 5: Final review, submit writeup before deadline |
| **Buffer** | Keep 2-3 days buffer before April 16 for unexpected issues |
