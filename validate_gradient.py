"""
Validation script for the EpistemicTrap-Metacog benchmark dataset.
Run BEFORE final submission to verify the dataset structure and distribution.
Expected output: "✅ All 150 items passed validation. Ready for submission."
"""
import json
import re
from collections import defaultdict


def load_dataset(path="metacog_dataset.json"):
    with open(path) as f:
        return json.load(f)


def validate_kbd_items(items):
    """Check: no item is trivially unknowable (too obvious) or trivially answerable."""
    issues = []
    for item in items:
        prompt = item["prompt"].lower()
        # Flag if prompt contains obviously fictional markers
        fiction_markers = ["wakanda", "fictional", "made-up", "hypothetical", "for this exercise"]
        for m in fiction_markers:
            if m in prompt:
                issues.append(f"KBD {item['id']}: Contains obvious fiction marker '{m}'")
        # Flag if prompt is under 80 chars (too short to be a real-sounding citation)
        if len(item["prompt"]) < 80:
            issues.append(f"KBD {item['id']}: Prompt too short ({len(item['prompt'])} chars) — may not be specific enough")
    return issues


def validate_ccc_items(items):
    """Check: all items have 3+ steps and confidence pattern is 'decreasing'."""
    issues = []
    for item in items:
        if len(item.get("steps", [])) < 3:
            issues.append(f"CCC {item['id']}: Fewer than 3 steps ({len(item.get('steps', []))})")
        if item.get("expected_confidence_pattern") != "decreasing":
            issues.append(f"CCC {item['id']}: expected_confidence_pattern is not 'decreasing'")
    return issues


def validate_cr_items(items):
    """Check: all items have an error_description and correct_answer."""
    issues = []
    for item in items:
        if not item.get("error_description"):
            issues.append(f"CR {item['id']}: Missing error_description")
        if not item.get("correct_answer"):
            issues.append(f"CR {item['id']}: Missing correct_answer")
    return issues


def validate_distribution(items):
    """Check subtype distribution meets minimum requirements."""
    counts = defaultdict(int)
    for item in items:
        counts[item["subtype"]] += 1
    print(f"Dataset distribution: {dict(counts)}")
    issues = []
    if counts["KBD"] < 50:
        issues.append(f"Not enough KBD items: {counts['KBD']} (need ≥50)")
    if counts["CCC"] < 40:
        issues.append(f"Not enough CCC items: {counts['CCC']} (need ≥40)")
    if counts["CR"] < 30:
        issues.append(f"Not enough CR items: {counts['CR']} (need ≥30)")
    return issues


if __name__ == "__main__":
    data = load_dataset()
    kbd = [x for x in data if x["subtype"] == "KBD"]
    ccc = [x for x in data if x["subtype"] == "CCC"]
    cr  = [x for x in data if x["subtype"] == "CR"]

    all_issues = []
    all_issues += validate_distribution(data)
    all_issues += validate_kbd_items(kbd)
    all_issues += validate_ccc_items(ccc)
    all_issues += validate_cr_items(cr)

    if all_issues:
        print(f"\n⚠️  {len(all_issues)} validation issues found:")
        for issue in all_issues:
            print(f"  - {issue}")
    else:
        print(f"\n✅ All {len(data)} items passed validation. Ready for submission.")
