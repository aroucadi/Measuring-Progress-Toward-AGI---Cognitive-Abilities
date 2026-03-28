# Complete Submission Guide: EpistemicTrap-Metacog v3.0 (MULTI-NOTEBOOK)
## Kaggle AGI Hackathon — Metacognition Track ($20K + $25K Grand Prize)

**Deadline: April 16, 2026**

> [!CAUTION]
> **KAGGLE ARCHITECTURE RULES (Updated via Official FAQ):**
> 1. You CANNOT have multiple tasks in one notebook.
> 2. You CANNOT use the "Import Notebook" feature.
> 3. You MUST evaluate against at least **5 different models**.

Because our benchmark has 4 tasks (KBD, CCC, CR, Pressure), you must create **4 separate Kaggle notebooks**, run them, and group them into a Benchmark. Follow every step in order.

**Rules-sensitive constraints (high impact)**
- Hackathon: one submission per team.
- Keep tasks/benchmark private until the deadline.
- External data/tools must be reasonably accessible and low cost.
- Winning submissions must be releasable under CC0 (avoid incompatible licenses).

---

## PHASE 1: Upload Your Datasets to Kaggle

1. Log into [kaggle.com](https://www.kaggle.com) with your `aroucadi` account.
2. Click **"+ Create"** → select **"New Dataset"**.
3. Upload **BOTH** files:
   - `metacog_dataset.json` (150 items: 60 KBD + 50 CCC + 40 CR)
   - `pressure_scenarios.json` (25 items)
4. Set title exactly to: **`metacog-dataset`**
5. Set visibility to **Private** and click **"Create"**.

---

## PHASE 2: Create the 4 Task Notebooks

You will repeat this process 4 times, once for each `.ipynb` file in your local directory (`1_kbd_task.ipynb`, `2_ccc_task.ipynb`, `3_cr_task.ipynb`, `4_pressure_task.ipynb`).

### Step 2.1 — Create the Notebook Environment
1. Navigate directly to: **https://www.kaggle.com/benchmarks/tasks/new**
   *(Do NOT import standard notebooks. Use this exact URL to load the SDK environment).*
2. Title the notebook: `EpistemicTrap-Metacog-KBD` (or CCC, CR, Pressure)
3. Under **"Input"** or **"Data"** (right panel), click **"+ Add Input"**. Search for your `metacog-dataset` and add it.

### Step 2.2 — Copy-Paste the Code Cell-by-Cell
4. Open your local `1_kbd_task.ipynb` file in VS Code or Jupyter.
5. In your Kaggle Task Notebook, delete any boilerplate code so it's empty.
6. **Copy Cell 1** from your local notebook and paste it into Kaggle Cell 1.
7. Click the **"+ Code"** button on Kaggle to create a new cell below.
8. **Copy Cell 2** from your local notebook and paste it into Kaggle Cell 2.
9. **Repeat this process** until all 5 cells from the local notebook are copied into their own respective cells on Kaggle.

### Step 2.3 — Run and Save
10. Click **"Run All"** (▶▶).
11. Wait for the run to complete. You should see it evaluate the items and print an analytics chart at the bottom!
12. Click **"Save Version"** (top right) → Choose **"Save & Run All (Commit)"**.
13. Wait for the version to finish saving (This takes a few minutes).

**REPEAT PHASE 2 FOR ALL 4 PYTHON NOTEBOOKS.**

---

## PHASE 3: Group into a Kaggle Benchmark

Now that you have 4 isolated tasks, you must group them so judges can grade the collective framework.

1. Go to **kaggle.com/benchmarks**.
2. Click **"Create Benchmark"**.
3. Title it: `EpistemicTrap-Metacog v3.0 (Behavioral Epistemic Integrity Suite)`
4. Add all 4 of your newly created tasks (KBD, CCC, CR, Pressure) to this collection.
5. Save the Benchmark.

---

## PHASE 4: Evaluate Against at least 5 Models

Kaggle's new rules **require** evaluation against 5 different models.

1. On your Benchmark page, look for **"Evaluate More Models"** (or do this on each Task's page).
2. Select 5 models covering different providers/sizes. **Our Recommended List:**
   - `gemini-2.0-flash` (Fast google baseline)
   - `gemini-2.5-pro` (Top google capability)
   - `claude-3-opus` (or `claude-3-5-sonnet` if available)
   - `llama-3-70b` (or 8B for open source)
   - `mistral-large` (or deepseek/qwen if you prefer)
   
   ⚠️ *Note: The FAQ says Gemma 3 does not support schemas. We DO NOT use schemas, but Gemma 3 may still struggle. Qwen3/GLM-5 do not support image inputs (we are text-only, so this is fine).*

3. Wait for the evaluations to finish. The platform will automatically manage your $50/day quota.

---

## PHASE 5: The Final Writeup

### Step 5.1 — Collect the 5-Model Data
After all models finish, check your 4 task leaderboards. Because the leaderboards only support single numerical values, all 4 of our tasks now output a normalized `float` (0.0 to 1.0).

Update your `writeup.md` to include the **REAL scores** for the 5 models you ran:
```markdown
| Model | KBD (60) | CCC (50) | CR (40) | Pressure (25) |
|---|---|---|---|---|
| gemini-2.0-flash | XX% | XX% | XX% | XX% |
| gemini-2.5-pro | XX% | XX% | XX% | XX% |
| claude-3-5-sonnet | XX% | XX% | XX% | XX% |
| llama-3-70b | XX% | XX% | XX% | XX% |
| deepseek-v2 | XX% | XX% | XX% | XX% |
```
*(Make sure finding narratives match your actual results.)*

## Optional: Regenerate & Validate Locally Before Upload
If you are editing datasets or prompts, regenerate and validate locally first:
- Regenerate: `py gen_kbd.py`, `py gen_ccc.py`, `py gen_cr.py`, then `py gen_combine.py`
- Validate: `py validate_gradient.py`

### Step 5.4 — Upload the Cover Image (Crucial Optics)
6. Under **"Media Gallery"**, upload the `kaggle_writeup_cover` image generated by your AI agent.
   - *Why?* Submissions with custom, high-quality thumbnails get significantly more clicks and judge attention on the Browse page.

### Step 5.5 — Link Your Open-Source GitHub
7. In the Writeup editor, find **"Project Links"** → **"GitHub Repository"**.
8. Paste: `https://github.com/aroucadi/Measuring-Progress-Toward-AGI---Cognitive-Abilities`
   - *Why?* Transparency. It proves to judges your code is rigorously version-controlled, not hacked together on the Kaggle UI in 5 minutes.

### Step 5.6 — SUBMIT
9. Click the green **"Submit"** button.
10. ⚠️ **Verify it says "Submitted"** — a draft will NOT be considered.
