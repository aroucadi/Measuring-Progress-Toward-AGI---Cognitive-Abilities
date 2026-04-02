import argparse
import csv
import glob
import json
import math
import os
import random
from collections import defaultdict


def _is_file(p: str) -> bool:
    try:
        return os.path.isfile(p)
    except Exception:
        return False


def find_run_logs(patterns: list[str]) -> list[str]:
    paths = set()
    for pat in patterns:
        for p in glob.glob(pat, recursive=True):
            if _is_file(p):
                paths.add(p)
    return sorted(paths)


def _safe_float(x):
    if x is None:
        return None
    try:
        return float(x)
    except Exception:
        return None


def extract_numeric_results(run_json: dict) -> list[float]:
    out = []
    for c in run_json.get("conversations", []) or []:
        r1 = c.get("result")
        if isinstance(r1, dict):
            nr = r1.get("numericResult")
            if isinstance(nr, dict):
                v = _safe_float(nr.get("value"))
                if v is not None:
                    out.append(v)
                    continue

        rs = c.get("results")
        if isinstance(rs, list):
            for r in rs:
                if not isinstance(r, dict):
                    continue
                nr = r.get("numericResult")
                if isinstance(nr, dict):
                    v = _safe_float(nr.get("value"))
                    if v is not None:
                        out.append(v)
    return out


def infer_task_name(run_json: dict, file_path: str) -> str:
    tv = run_json.get("taskVersion")
    if isinstance(tv, dict):
        name = tv.get("name")
        if isinstance(name, str) and name.strip():
            return name.strip()
    t = run_json.get("task")
    if isinstance(t, dict):
        name = t.get("name")
        if isinstance(name, str) and name.strip():
            return name.strip()
    for k in ["taskName", "task_name", "benchmarkTaskName"]:
        v = run_json.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    base = os.path.basename(file_path)
    return os.path.splitext(base)[0]


def infer_model_name(run_json: dict) -> str:
    m = run_json.get("model")
    if isinstance(m, dict):
        name = m.get("name")
        if isinstance(name, str) and name.strip():
            return name.strip()
    for k in ["modelName", "model_name", "llmName", "llm_name"]:
        v = run_json.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    rp = run_json.get("runParams") or run_json.get("run_params")
    if isinstance(rp, dict):
        for k in ["model", "modelName", "llm", "llmName", "name"]:
            v = rp.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
            if isinstance(v, dict):
                name = v.get("name")
                if isinstance(name, str) and name.strip():
                    return name.strip()
    return "unknown_model"


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def stdev(xs: list[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def bootstrap_mean_ci(xs: list[float], iters: int, alpha: float, rng: random.Random):
    if not xs:
        return None
    n = len(xs)
    mu = mean(xs)
    means = []
    for _ in range(iters):
        s = 0.0
        for _ in range(n):
            s += xs[rng.randrange(n)]
        means.append(s / n)
    means.sort()
    lo = means[int((alpha / 2) * iters)]
    hi = means[int((1 - alpha / 2) * iters) - 1]
    return (mu, lo, hi)


def bootstrap_diff_ci(a: list[float], b: list[float], iters: int, alpha: float, rng: random.Random):
    if not a or not b:
        return None
    na = len(a)
    nb = len(b)
    diffs = []
    for _ in range(iters):
        sa = 0.0
        for _ in range(na):
            sa += a[rng.randrange(na)]
        sb = 0.0
        for _ in range(nb):
            sb += b[rng.randrange(nb)]
        diffs.append((sa / na) - (sb / nb))
    diffs.sort()
    mu = mean(a) - mean(b)
    lo = diffs[int((alpha / 2) * iters)]
    hi = diffs[int((1 - alpha / 2) * iters) - 1]
    return (mu, lo, hi)


def to_markdown_table(rows: list[list[str]], headers: list[str]) -> str:
    out = []
    out.append("| " + " | ".join(headers) + " |")
    out.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--glob", action="append", default=["*.run.json", "**/*.run.json"])
    ap.add_argument("--out-md", default="results.md")
    ap.add_argument("--out-csv", default="results.csv")
    ap.add_argument("--out-diff-csv", default="pairwise_diffs.csv")
    ap.add_argument("--bootstrap-iters", type=int, default=2000)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--seed", type=int, default=20260328)
    ap.add_argument("--pairwise", action="store_true", default=True)
    args = ap.parse_args(argv)

    rng = random.Random(args.seed)
    paths = find_run_logs(args.glob)
    if not paths:
        with open(args.out_md, "w", encoding="utf-8") as f:
            f.write("No *.run.json files found.\n")
        with open(args.out_csv, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["task", "model", "n", "mean", "ci_lo", "ci_hi", "sd", "se"])
        if args.pairwise:
            with open(args.out_diff_csv, "w", encoding="utf-8", newline="") as f:
                w = csv.writer(f)
                w.writerow(["task", "model_a", "model_b", "diff_mean", "diff_ci_lo", "diff_ci_hi"])
        return 0

    by_task_model = defaultdict(list)
    for p in paths:
        try:
            with open(p, "r", encoding="utf-8") as f:
                run = json.load(f)
        except Exception:
            continue
        vals = extract_numeric_results(run)
        if not vals:
            continue
        task = infer_task_name(run, p)
        model = infer_model_name(run)
        by_task_model[(task, model)].extend(vals)

    summary_rows = []
    csv_rows = []
    for (task, model), vals in sorted(by_task_model.items()):
        ci = bootstrap_mean_ci(vals, args.bootstrap_iters, args.alpha, rng)
        if not ci:
            continue
        mu, lo, hi = ci
        sd = stdev(vals)
        se = sd / math.sqrt(len(vals)) if len(vals) > 0 else 0.0
        summary_rows.append([task, model, str(len(vals)), f"{mu:.3f} [{lo:.3f}, {hi:.3f}]"])
        csv_rows.append([task, model, len(vals), mu, lo, hi, sd, se])

    md = []
    md.append("# Results Summary\n\n")
    md.append(f"Bootstrap: iters={args.bootstrap_iters}, alpha={args.alpha}, seed={args.seed}\n\n")
    md.append(to_markdown_table(summary_rows, ["task", "model", "n", "score_mean_ci"]))
    md.append("\n")

    with open(args.out_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["task", "model", "n", "mean", "ci_lo", "ci_hi", "sd", "se"])
        for r in csv_rows:
            w.writerow(r)

    if args.pairwise:
        diff_rows = []
        for task in sorted({t for (t, _) in by_task_model.keys()}):
            models = sorted({m for (t, m) in by_task_model.keys() if t == task})
            for i in range(len(models)):
                for j in range(i + 1, len(models)):
                    a = by_task_model[(task, models[i])]
                    b = by_task_model[(task, models[j])]
                    dci = bootstrap_diff_ci(a, b, args.bootstrap_iters, args.alpha, rng)
                    if not dci:
                        continue
                    dmu, dlo, dhi = dci
                    diff_rows.append([task, models[i], models[j], dmu, dlo, dhi])

        diff_rows_sorted = sorted(diff_rows, key=lambda r: abs(r[3]), reverse=True)
        diff_md_rows = []
        for task, ma, mb, dmu, dlo, dhi in diff_rows_sorted[:50]:
            diff_md_rows.append([task, ma, mb, f"{dmu:.3f} [{dlo:.3f}, {dhi:.3f}]"])
        if diff_md_rows:
            md.append("## Pairwise Differences (Top 50 by |diff|)\n\n")
            md.append(to_markdown_table(diff_md_rows, ["task", "model_a", "model_b", "diff_mean_ci"]))
            md.append("\n")

        with open(args.out_diff_csv, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["task", "model_a", "model_b", "diff_mean", "diff_ci_lo", "diff_ci_hi"])
            for r in diff_rows:
                w.writerow(r)

    with open(args.out_md, "w", encoding="utf-8") as f:
        f.write("".join(md))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
