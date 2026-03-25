# Official Submission Guide: Kaggle AGI Hackathon (Metacognition Track)

This guide walks you step-by-step through uploading the deliverables we created to the Kaggle Benchmarks platform, explicitly following the `kaggle-benchmarks` SDK documentation.

---

## 🛑 Phase 1: Upload Your Custom Dataset
Before you can build the benchmark, your raw data must exist in Kaggle's ecosystem.

1. Log into your Kaggle account.
2. In the left-hand navigation menu, click **Create** (+ icon) > **Dataset**.
3. In the upload window, drag and drop the `metacog_dataset.json` file we generated locally.
4. Title your dataset appropriately (e.g., `Metacognition-AGI-Epistemic-Traps`).
5. **CRITICAL:** Ensure the privacy setting in the bottom-left corner remains set to **Private**. (It will automatically become public after the deadline.)
6. Click **Create** to finalize the dataset.

---

## 🛠️ Phase 2: Create the Kaggle Benchmark
Kaggle evaluates submissions using their proprietary Benchmarks web app. You must physically create the benchmark entity on their servers using our code.

1. Navigate directly to the Kaggle Benchmarks hub: [kaggle.com/benchmarks](https://www.kaggle.com/benchmarks).
2. Click the **"New Benchmark"** button in the top right. This spins up a specialized Kaggle Notebook pre-configured for the `kaggle-benchmarks` SDK.
3. Give your notebook a descriptive title at the top left (e.g., `EpistemicTrap-Metacog-Benchmark`).

### Attach Your Dataset
4. In your new benchmark notebook, look at the right-hand **Notebook Options Panel**.
5. Click **"Add Input"**.
6. Search for the `Metacognition-AGI-Epistemic-Traps` dataset you created in Phase 1. Click the **+** button to attach it to your working environment.

### Inject the Code
7. Open our local file `benchmark_metacognition.ipynb`.
8. Copy the Python code from our local cells and paste it directly into the cells of your new Kaggle Notebook.
    * *Note that our code already imports `kaggle_benchmarks as kbench`, uses `@kbench.task`, and ends with the `%choose metacog_kbd` magic command, which perfectly aligns with the SDK requirements.*
    * **Important Pathing Note:** Ensure `filepath` in cell 1 points accurately to where Kaggle mounted your dataset (usually `/kaggle/input/YOUR-DATASET-NAME/metacog_dataset.json`). Adjust the string slightly in cell 1 if necessary.

### Run and Save
9. Click **"Run All"** to execute your code.
10. At the bottom of the notebook, you should see the official **Kaggle Benchmark UI Widget** render. This proves your tasks are perfectly formatted for the leaderboard!
11. Click the **"Save Version"** (or Publish) button in the top right corner.
12. Ensure the Notebook visibility is set to **Private** before saving.

---

## 📝 Phase 3: Submit Your Final Writeup
This is the official action that enters you into the $200,000 prize pool.

1. Go directly to the **Measuring AGI Hackathon** [Submission Platform](https://www.kaggle.com/competitions/kaggle-measuring-agi/overview).
2. Click the **"New Writeup"** button on the competition page.
3. **Select your Track:** explicitly check the box for **"Metacognition"**.
4. **Paste the Report:** Open our local `writeup.md` file, copy all the text, and paste it into the Kaggle main text editor.

### Link the Benchmark (Mandatory Step)
5. On the right-hand panel of the Writeup editor, locate the **"Project Links"** or **"Attachments"** section.
6. Click **"Add a link"**.
7. In the panel that opens, select **"Benchmark"** and choose the `EpistemicTrap-Metacog-Benchmark` you just saved in Phase 2. This ties your written report to your executable code.

### Add a Cover Image (Optional but Highly Recommended)
8. Under the **"Media Gallery"** section, attach a high-quality cover image (e.g., an abstract brain, maze, or "epistemic trap" graphic) to make your submission visually premium for the judges.

### Final Submission
9. Click the green **"Submit"** button in the top right corner of the Writeup page.

✅ **Congratulations!** Your benchmark is now officially in the running for the Metacognition Track prize.
