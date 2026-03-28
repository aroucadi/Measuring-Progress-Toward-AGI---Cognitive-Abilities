# -*- coding: utf-8 -*-
"""
Extended validation script for EpistemicTrap-Metacog v2
Validates all 4 task datasets before Kaggle submission
"""
import json
import re
import sys
from collections import defaultdict

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def validate_kbd(items):
    issues = []
    FICTION_MARKERS = ["wakanda", "fictional", "hypothetical", "for this exercise",
                       "made-up", "imaginary", "placeholder", "example only"]
    KBIA_PATTERN = re.compile(r"KBIA-ID:\s*KBIA-2026-[0-9a-f]{12}")

    for item in items:
        prompt = item.get("prompt", "")
        if len(prompt) < 80:
            issues.append(f"KBD {item['id']}: Prompt too short ({len(prompt)} chars)")
        for marker in FICTION_MARKERS:
            if marker.lower() in prompt.lower():
                issues.append(f"KBD {item['id']}: Contains fiction marker '{marker}'")
        if not KBIA_PATTERN.search(prompt):
            issues.append(f"KBD {item['id']}: Missing KBIA-ID pattern (KBIA-2026-xxxxxxxxxxxx)")
        for field in ["id", "subtype", "prompt", "ground_truth_signal", "difficulty"]:
            if not item.get(field):
                issues.append(f"KBD {item['id']}: Missing field '{field}'")
        if item.get("difficulty") not in ["easy", "medium", "hard"]:
            issues.append(f"KBD {item['id']}: Invalid difficulty '{item.get('difficulty')}'")
    return issues

def validate_ccc(items):
    issues = []
    for item in items:
        steps = item.get("steps", [])
        if len(steps) < 3:
            issues.append(f"CCC {item['id']}: Fewer than 3 steps ({len(steps)})")
        if item.get("answer_type") not in {"int", "fraction", "decimal"}:
            issues.append(f"CCC {item.get('id', '?')}: Invalid answer_type '{item.get('answer_type')}'")
        if item.get("difficulty") not in {"easy", "medium", "hard"}:
            issues.append(f"CCC {item.get('id', '?')}: Invalid difficulty '{item.get('difficulty')}'")
        for field in ["id", "subtype", "prompt", "steps", "final_answer", "answer_type", "difficulty"]:
            if field not in item or item[field] is None or (isinstance(item[field], str) and not item[field].strip()):
                issues.append(f"CCC {item.get('id', '?')}: Missing field '{field}'")
        for s in steps:
            if not isinstance(s, dict) or not s.get("question") or not s.get("answer"):
                issues.append(f"CCC {item['id']}: Invalid step schema")
    return issues

def validate_cr(items):
    issues = []
    VALID_DIFFICULTY = {"easy", "medium", "hard"}
    for item in items:
        for field in ["id", "subtype", "prompt", "error_location", "correction", "difficulty"]:
            if field not in item or item[field] is None or (isinstance(item[field], str) and not item[field].strip()):
                issues.append(f"CR {item.get('id', '?')}: Missing field '{field}'")
        if item.get("difficulty") not in VALID_DIFFICULTY:
            issues.append(f"CR {item.get('id', '?')}: Invalid difficulty '{item.get('difficulty')}'")
        if not re.search(r"\[L\d+\]", item.get("prompt", "")):
            issues.append(f"CR {item.get('id', '?')}: Missing line labels in prompt")
    return issues

def validate_pressure(items):
    issues = []
    REQUIRED = [
        "id",
        "type",
        "initial_question",
        "pressure_claim",
        "authority_claim",
        "expected_stance",
        "correct_epistemic_stance",
        "references",
        "answer_format",
    ]
    for item in items:
        for field in REQUIRED:
            if field not in item or item[field] is None or (isinstance(item[field], str) and not item[field].strip()):
                issues.append(f"Pressure {item.get('id', '?')}: Missing field '{field}'")
        if item.get("type") not in {"knowable", "needs_clarification"}:
            issues.append(f"Pressure {item.get('id', '?')}: Invalid type '{item.get('type')}'")
        if item.get("expected_stance") not in {"MAINTAIN_CORRECT", "ASK_CLARIFY"}:
            issues.append(f"Pressure {item.get('id', '?')}: Invalid expected_stance '{item.get('expected_stance')}'")
        if item.get("type") == "knowable" and not item.get("gold_answer"):
            issues.append(f"Pressure {item.get('id', '?')}: Missing gold_answer for knowable item")
        if len(item.get("initial_question", "")) < 40:
            issues.append(f"Pressure {item['id']}: initial_question too short")
        if len(item.get("pressure_claim", "")) < 20:
            issues.append(f"Pressure {item['id']}: pressure_claim too vague")
        if len(item.get("authority_claim", "")) < 20:
            issues.append(f"Pressure {item['id']}: authority_claim too vague")
        if len(item.get("correct_epistemic_stance", "")) < 40:
            issues.append(f"Pressure {item['id']}: correct_epistemic_stance too short")
    return issues

def validate_distribution(main_data, pressure_data):
    counts = defaultdict(int)
    for item in main_data:
        counts[item["subtype"]] += 1
    print(f"  Dataset distribution: {dict(counts)}")
    print(f"  Pressure scenarios:   {len(pressure_data)}")
    issues = []
    if counts["KBD"] < 50: issues.append(f"Not enough KBD items: {counts['KBD']} (need >= 50)")
    if counts["CCC"] < 40: issues.append(f"Not enough CCC items: {counts['CCC']} (need >= 40)")
    if counts["CR"]  < 30: issues.append(f"Not enough CR items: {counts['CR']} (need >= 30)")
    if len(pressure_data) < 20: issues.append(f"Not enough Pressure items: {len(pressure_data)} (need >= 20)")
    return issues

def validate_unique_ids(main_data, pressure_data):
    ids = [item["id"] for item in main_data] + [item["id"] for item in pressure_data]
    dupes = [x for x in set(ids) if ids.count(x) > 1]
    return [f"Duplicate ID: {d}" for d in dupes]

if __name__ == "__main__":
    print("EpistemicTrap-Metacog v2 — Dataset Validation")
    print("=" * 50)

    main_data = load_json("metacog_dataset.json")
    pressure_data = load_json("pressure_scenarios.json")

    kbd = [x for x in main_data if x["subtype"] == "KBD"]
    ccc = [x for x in main_data if x["subtype"] == "CCC"]
    cr  = [x for x in main_data if x["subtype"] == "CR"]

    all_issues = []
    all_issues += validate_distribution(main_data, pressure_data)
    all_issues += validate_unique_ids(main_data, pressure_data)
    all_issues += validate_kbd(kbd)
    all_issues += validate_ccc(ccc)
    all_issues += validate_cr(cr)
    all_issues += validate_pressure(pressure_data)

    if all_issues:
        print(f"\n  {len(all_issues)} validation issues found:")
        for issue in all_issues:
            print(f"    - {issue}")
        sys.exit(1)
    else:
        total = len(main_data) + len(pressure_data)
        print(f"\n  All {total} items passed validation. Ready for Kaggle submission.")
