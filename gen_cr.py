"""Generate CR items (40) for metacog_dataset.json"""
import json
import math
import random

random.seed(20260328)

items = []


def add_item(i: int, prompt: str, error_location: str, correction: str, difficulty: str):
    items.append(
        {
            "id": f"cr_{i:03d}",
            "subtype": "CR",
            "prompt": prompt,
            "error_location": error_location,
            "correction": correction,
            "difficulty": difficulty,
        }
    )


def make_header(task: str) -> str:
    return (
        "You are reviewing a short reasoning transcript that contains exactly ONE error.\n"
        "Your job is to locate the error and provide the correction.\n"
        "Output a SINGLE JSON object on the last line with keys: error_location, correction.\n"
        "error_location must be one of the line labels like \"L3\".\n\n"
        f"Task: {task}\n\n"
    )


idx = 1

for _ in range(8):
    a = random.randint(12, 99)
    b = random.randint(12, 99)
    c = random.randint(2, 9)
    correct1 = a + b
    correct2 = correct1 * c
    wrong2 = correct2 + random.choice([-c, c, -2 * c, 2 * c])
    prompt = make_header(f"Compute ({a} + {b}) * {c}.") + "\n".join(
        [
            f"[L1] Start by adding: {a} + {b} = {correct1}.",
            f"[L2] Multiply by {c}: {correct1} * {c} = {wrong2}.",
            f"[L3] Therefore the final answer is {wrong2}.",
        ]
    )
    add_item(idx, prompt, "L2", f"{correct1} * {c} = {correct2}", "easy")
    idx += 1

for _ in range(8):
    p = random.choice([3, 4, 5, 6, 7, 8, 9, 10])
    q = random.choice([3, 4, 5, 6, 7, 8, 9, 10])
    while q == p:
        q = random.choice([3, 4, 5, 6, 7, 8, 9, 10])
    num = q + p
    den = p * q
    g = math.gcd(num, den)
    num_r, den_r = num // g, den // g
    wrong_den = den + random.choice([-p, p, -q, q])
    prompt = make_header(f"Compute 1/{p} + 1/{q} as a reduced fraction.") + "\n".join(
        [
            f"[L1] Common denominator is {p}*{q} = {den}.",
            f"[L2] Convert: 1/{p} = {q}/{den} and 1/{q} = {p}/{den}.",
            f"[L3] Add numerators: {q}+{p} = {num}, so the sum is {num}/{wrong_den}.",
            f"[L4] Reduced form is {num}/{wrong_den}.",
        ]
    )
    add_item(idx, prompt, "L3", f"{num}/{den} reduces to {num_r}/{den_r}", "medium")
    idx += 1

for _ in range(8):
    a = random.randint(2, 9)
    b = random.randint(2, 9)
    correct = a ** b
    wrong = correct + random.choice([-a, a, -b, b])
    prompt = make_header(f"Compute {a}^{b}.") + "\n".join(
        [
            f"[L1] {a}^{b} means multiplying {a} by itself {b} times.",
            f"[L2] So {a}^{b} = {wrong}.",
            f"[L3] Final answer: {wrong}.",
        ]
    )
    add_item(idx, prompt, "L2", f"{a}^{b} = {correct}", "medium")
    idx += 1

for _ in range(8):
    n = random.randint(4, 8)
    k = random.randint(0, n)
    ways = math.comb(n, k)
    total = 2 ** n
    correct = f"{ways}/{total}"
    wrong_ways = max(0, ways + random.choice([-2, -1, 1, 2]))
    prompt = make_header(f"For a fair coin flipped {n} times, compute P(exactly {k} heads) as a reduced fraction.") + "\n".join(
        [
            f"[L1] Number of ways to choose {k} heads out of {n} flips is C({n},{k}) = {wrong_ways}.",
            f"[L2] Total outcomes is 2^{n} = {total}.",
            f"[L3] Probability is {wrong_ways}/{total}.",
        ]
    )
    add_item(idx, prompt, "L1", f"C({n},{k}) = {ways}; probability = {correct}", "hard")
    idx += 1

for _ in range(8):
    a = random.randint(20, 200)
    b = random.randint(2, 9)
    r = a % b
    wrong = (r + 1) % b
    prompt = make_header(f"Compute {a} mod {b}.") + "\n".join(
        [
            f"[L1] The remainder when {a} is divided by {b} is {wrong}.",
            f"[L2] Therefore {a} mod {b} = {wrong}.",
        ]
    )
    add_item(idx, prompt, "L1", f"{a} mod {b} = {r}", "easy")
    idx += 1

with open("_cr_items.json", "w", encoding="utf-8") as f:
    json.dump(items, f, indent=2, ensure_ascii=False)
print(f"Wrote {len(items)} CR items")
