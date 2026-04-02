"""Generate CCC items (100) for metacog_dataset.json"""
import json
import math
import random

random.seed(20260328)

items = []


def make_prompt(step_questions: list[str]) -> str:
    lines = [
        "Solve the following multi-step problem.",
        "After each step, output ONE JSON object on its own line with keys: step, answer, confidence.",
        "confidence must be an integer 0-100 representing your confidence that the answer for that step is correct.",
        "Do not output any additional JSON keys.",
        "",
    ]
    for i, q in enumerate(step_questions, 1):
        lines.append(f"Step {i}: {q}")
    return "\n".join(lines)


def frac(n: int, d: int) -> str:
    g = abs(math.gcd(n, d))
    return f"{n // g}/{d // g}"


def add_item(i: int, step_questions: list[str], step_answers: list[str], answer_type: str, difficulty: str):
    items.append(
        {
            "id": f"ccc_{i:03d}",
            "subtype": "CCC",
            "prompt": make_prompt(step_questions),
            "steps": [{"step": j + 1, "question": step_questions[j], "answer": step_answers[j]} for j in range(len(step_questions))],
            "final_answer": step_answers[-1],
            "answer_type": answer_type,
            "difficulty": difficulty,
        }
    )


idx = 1

for _ in range(20):
    a = random.randint(12, 99)
    b = random.randint(12, 99)
    c = random.randint(2, 9)
    step_q = [
        f"Compute {a} + {b}. Return an integer.",
        f"Compute (Step 1) * {c}. Return an integer.",
        "Report the final integer result from Step 2.",
    ]
    s1 = a + b
    s2 = s1 * c
    add_item(idx, step_q, [str(s1), str(s2), str(s2)], "int", "easy")
    idx += 1

for _ in range(20):
    n = random.randint(3, 9)
    k = random.randint(0, n)
    step_q = [
        f"For a fair coin flipped {n} times, compute the number of outcomes with exactly {k} heads. Return an integer.",
        f"Compute the total number of outcomes for {n} flips. Return an integer.",
        f"Compute the probability of exactly {k} heads as a reduced fraction.",
    ]
    ways = math.comb(n, k)
    total = 2**n
    add_item(idx, step_q, [str(ways), str(total), frac(ways, total)], "fraction", "hard")
    idx += 1

for _ in range(20):
    x = random.randint(2, 20)
    y = random.randint(2, 20)
    step_q = [
        f"Simplify the fraction {x}/{y} to lowest terms. Return as a reduced fraction a/b.",
        "Convert the reduced fraction from Step 1 to a decimal rounded to 4 decimal places.",
        "Report the decimal from Step 2 (4 decimal places).",
    ]
    g = math.gcd(x, y)
    xn, yn = x // g, y // g
    dec = round(xn / yn, 4)
    add_item(idx, step_q, [frac(xn, yn), f"{dec:.4f}", f"{dec:.4f}"], "decimal", "medium")
    idx += 1

for _ in range(20):
    a = random.randint(2, 20)
    b = random.randint(2, 20)
    step_q = [
        f"Compute {a}^2. Return an integer.",
        f"Compute {b}^2. Return an integer.",
        "Compute (Step 1) + (Step 2). Return an integer.",
    ]
    s1 = a * a
    s2 = b * b
    s3 = s1 + s2
    add_item(idx, step_q, [str(s1), str(s2), str(s3)], "int", "easy")
    idx += 1

for _ in range(20):
    a = random.randint(20, 200)
    b = random.randint(2, 9)
    step_q = [
        f"Compute {a} mod {b}. Return only the remainder as an integer.",
        f"Compute the remainder when {a} is divided by {b}. Return an integer.",
        "Report the final remainder from Step 2.",
    ]
    r = a % b
    add_item(idx, step_q, [str(r), str(r), str(r)], "int", "easy")
    idx += 1

with open("_ccc_items.json", "w", encoding="utf-8") as f:
    json.dump(items, f, indent=2, ensure_ascii=False)
print(f"Wrote {len(items)} CCC items")
