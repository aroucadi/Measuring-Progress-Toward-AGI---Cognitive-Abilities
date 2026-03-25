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
    DOI_PATTERN = re.compile(r"10\.\d{4,}/\S+")

    for item in items:
        prompt = item.get("prompt", "")
        if len(prompt) < 80:
            issues.append(f"KBD {item['id']}: Prompt too short ({len(prompt)} chars)")
        for marker in FICTION_MARKERS:
            if marker.lower() in prompt.lower():
                issues.append(f"KBD {item['id']}: Contains fiction marker '{marker}'")
        if not DOI_PATTERN.search(prompt):
            issues.append(f"KBD {item['id']}: Missing valid DOI pattern (10.XXXX/...)")
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
        if item.get("expected_confidence_pattern") != "decreasing":
            issues.append(f"CCC {item['id']}: expected_confidence_pattern != 'decreasing'")
        for field in ["id", "subtype", "prompt", "steps", "expected_confidence_pattern"]:
            if not item.get(field):
                issues.append(f"CCC {item['id']}: Missing field '{field}'")
    return issues

def validate_cr(items):
    issues = []
    VALID_TYPES = {"date", "causality", "unit", "attribution", "statistic"}
    VALID_SUBTLETY = {"obvious", "medium", "subtle"}
    for item in items:
        if not item.get("error_description"):
            issues.append(f"CR {item['id']}: Missing error_description")
        if not item.get("correct_answer"):
            issues.append(f"CR {item['id']}: Missing correct_answer")
        if item.get("error_type") not in VALID_TYPES:
            issues.append(f"CR {item['id']}: Invalid error_type '{item.get('error_type')}'")
        if item.get("error_subtlety") not in VALID_SUBTLETY:
            issues.append(f"CR {item['id']}: Invalid error_subtlety '{item.get('error_subtlety')}'")
    return issues

def validate_pressure(items):
    issues = []
    REQUIRED = ["id", "initial_question", "pressure_claim", "authority_claim",
                 "correct_epistemic_stance"]
    for item in items:
        for field in REQUIRED:
            if not item.get(field):
                issues.append(f"Pressure {item.get('id', '?')}: Missing field '{field}'")
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
