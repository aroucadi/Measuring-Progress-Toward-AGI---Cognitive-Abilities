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

# -- Batch 5a: Drug dosage chains (5 items) --
# Each step propagates uncertainty: weight→dose→adjustment→rounding
dosage_params = [
    (70, 5, 0.8, 50),   # 70 kg, 5 mg/kg, 80% renal, round to 50mg
    (85, 3, 0.6, 25),   # 85 kg, 3 mg/kg, 60% renal, round to 25mg
    (60, 8, 0.7, 100),  # 60 kg, 8 mg/kg, 70% hepatic, round to 100mg
    (95, 4, 0.9, 50),   # 95 kg, 4 mg/kg, 90% renal, round to 50mg
    (55, 6, 0.5, 25),   # 55 kg, 6 mg/kg, 50% renal, round to 25mg
]
for weight, dose_per_kg, clearance, round_to in dosage_params:
    raw = weight * dose_per_kg
    adjusted = raw * clearance
    import math as _math
    final = round(adjusted / round_to) * round_to
    step_q = [
        f"A patient weighs {weight} kg. The standard dose is {dose_per_kg} mg/kg. Compute the raw dose in mg. Return an integer.",
        f"The patient has reduced organ function requiring a {clearance} adjustment factor. Multiply the raw dose from Step 1 by {clearance}. Return a number (decimal ok).",
        f"Round the adjusted dose from Step 2 to the nearest {round_to} mg. Return an integer.",
    ]
    add_item(idx, step_q, [str(raw), str(adjusted), str(final)], "int", "medium")
    idx += 1

# -- Batch 5b: Compound probability chains (5 items) --
# P(A) * P(B|A) * P(C|A∩B) — uncertainty genuinely compounds
compound_params = [
    (30, 50, 40),  # P(rain)=0.30, P(delay|rain)=0.50, P(cancel|delay)=0.40
    (20, 60, 30),  # P(defect)=0.20, P(fail|defect)=0.60, P(recall|fail)=0.30
    (40, 70, 50),  # P(infection)=0.40, P(resistant|inf)=0.70, P(ICU|resistant)=0.50
    (15, 80, 25),  # P(flaw)=0.15, P(exploit|flaw)=0.80, P(breach|exploit)=0.25
    (50, 30, 60),  # P(cloud)=0.50, P(rain|cloud)=0.30, P(flood|rain)=0.60
]
prob_labels = [
    ("rain", "flight delay given rain", "cancellation given delay"),
    ("manufacturing defect", "component failure given defect", "product recall given failure"),
    ("infection", "antibiotic resistance given infection", "ICU admission given resistance"),
    ("software flaw", "exploit given flaw", "data breach given exploit"),
    ("cloud cover", "rain given cloud cover", "flash flood given rain"),
]
for (p1, p2, p3), (l1, l2, l3) in zip(compound_params, prob_labels):
    r1 = p1 / 100
    r2 = p2 / 100
    r3 = p3 / 100
    joint_12 = round(r1 * r2, 4)
    joint_123 = round(r1 * r2 * r3, 4)
    step_q = [
        f"The probability of {l1} is {p1}%. The probability of {l2} is {p2}%. Compute P({l1} AND {l2}). Return as a decimal rounded to 4 places.",
        f"Given P({l1} AND {l2}) from Step 1, and P({l3}) is {p3}%, compute P(all three events). Return as a decimal rounded to 4 places.",
        f"Express the probability from Step 2 as a percentage rounded to 2 decimal places. Return the number only (no % sign).",
    ]
    pct = round(joint_123 * 100, 2)
    add_item(idx, step_q, [f"{joint_12:.4f}", f"{joint_123:.4f}", f"{pct:.2f}"], "decimal", "hard")
    idx += 1

# -- Batch 5c: Multi-step Fermi estimation chains (5 items) --
# Each step builds on the previous; error propagates
fermi_chains = [
    # Water usage: liters/flush * flushes/day * days/year
    (6, 5, 365,
     "A standard toilet uses 6 liters per flush. Compute the water used in 5 flushes. Return an integer.",
     "A person flushes approximately 5 times per day. Using the per-day water from Step 1, compute the total liters used in one year (365 days). Return an integer.",
     "If water costs $0.003 per liter, compute the annual toilet-water cost from Step 2 in dollars. Return a number rounded to 2 decimal places."),
    # Energy: watts * hours/day * days/month → kWh
    (60, 8, 30,
     "A light bulb uses 60 watts. If it runs for 8 hours, compute the energy in watt-hours. Return an integer.",
     "Compute the monthly energy (30 days) at 8 hours/day from Step 1, in watt-hours. Return an integer.",
     "Convert the watt-hours from Step 2 to kilowatt-hours. Return a number rounded to 1 decimal place."),
    # Coffee: cups/day * mL/cup * days → liters
    (3, 250, 365,
     "A person drinks 3 cups of coffee per day, each 250 mL. Compute daily coffee in mL. Return an integer.",
     "Compute the annual coffee consumption from Step 1 in mL (365 days). Return an integer.",
     "Convert the annual mL from Step 2 to liters. Return a number rounded to 1 decimal place."),
    # Car distance: km/day * days/week * weeks/year
    (40, 5, 50,
     "A commuter drives 40 km per workday. Compute the weekly distance for a 5-day work week in km. Return an integer.",
     "Compute the annual distance from Step 1 assuming 50 working weeks per year. Return an integer.",
     "If fuel costs $0.12 per km, compute the annual fuel cost from Step 2 in dollars. Return an integer."),
    # Typing: wpm * minutes * characters/word
    (80, 45, 5,
     "A typist types 80 words per minute. Compute the words typed in a 45-minute session. Return an integer.",
     "Assuming an average of 5 characters per word, compute the total characters from Step 1. Return an integer.",
     "If each character takes 2 bytes of storage, compute the total bytes from Step 2. Return an integer."),
]
for (a, b, c, q1, q2, q3) in fermi_chains:
    s1 = a * b
    s2 = s1 * c
    # Step 3 answer depends on which chain
    if a == 6:  # water cost
        s3 = f"{round(s2 * 0.003, 2):.2f}"
        atype = "decimal"
    elif a == 60:  # kWh
        s3 = f"{round(s2 / 1000, 1):.1f}"
        atype = "decimal"
    elif a == 3:  # liters
        s3 = f"{round(s2 / 1000, 1):.1f}"
        atype = "decimal"
    elif a == 40:  # fuel cost
        s3 = str(round(s2 * 0.12))
        atype = "int"
    else:  # bytes
        s3 = str(s2 * 2)
        atype = "int"
    add_item(idx, [q1, q2, q3], [str(s1), str(s2), s3], atype, "medium")
    idx += 1

# -- Batch 5d: Unit conversion chains (5 items) --
# Error in step 1 propagates through steps 2 and 3
conversion_chains = [
    # miles → km → time → ETA
    ("Convert 12 miles to kilometers (1 mile = 1.609 km). Return a number rounded to 2 decimal places.",
     "At a speed of 60 km/h, compute the travel time for the distance from Step 1 in minutes. Return a number rounded to 1 decimal place.",
     "If departure is at 14:00 and travel takes the time from Step 2, plus a 10-minute buffer, what is the arrival time in HH:MM format?",
     [f"{round(12 * 1.609, 2):.2f}", f"{round(12 * 1.609 / 60 * 60, 1):.1f}", "14:29"],
     "time", "medium"),
    # Fahrenheit → Celsius → Kelvin
    ("Convert 212°F to Celsius using C = (F-32)*5/9. Return an integer.",
     "Convert the Celsius from Step 1 to Kelvin (K = C + 273.15). Return a number rounded to 2 decimal places.",
     "Is the Kelvin value from Step 2 above or below the boiling point of ethanol (351.44 K)? Answer 'above' or 'below'.",
     ["100", "373.15", "above"],
     "text", "medium"),
    # pounds → kg → BMI
    ("Convert 176 pounds to kilograms (1 lb = 0.4536 kg). Return a number rounded to 1 decimal place.",
     "A person is 1.75 m tall and weighs the kg from Step 1. Compute BMI = weight/(height^2). Return a number rounded to 1 decimal place.",
     "Classify the BMI from Step 2: 'underweight' (<18.5), 'normal' (18.5-24.9), 'overweight' (25-29.9), or 'obese' (>=30). Return only the category.",
     [f"{round(176 * 0.4536, 1):.1f}", f"{round(176 * 0.4536 / (1.75**2), 1):.1f}", "overweight" if 25 <= round(176 * 0.4536 / (1.75**2), 1) < 30 else "normal"],
     "text", "medium"),
    # gallons → liters → mL
    ("Convert 3 US gallons to liters (1 gal = 3.785 L). Return a number rounded to 3 decimal places.",
     "Convert the liters from Step 1 to milliliters. Return a number rounded to 0 decimal places (integer).",
     "If a dose is 15 mL, compute how many full doses can be obtained from Step 2. Return an integer (floor).",
     [f"{round(3 * 3.785, 3):.3f}", str(round(3 * 3.785 * 1000)), str(int(3 * 3.785 * 1000 / 15))],
     "int", "medium"),
    # meters/second → km/h → mph
    ("Convert 25 m/s to km/h (multiply by 3.6). Return an integer.",
     "Convert the km/h from Step 1 to mph (1 km = 0.6214 miles). Return a number rounded to 1 decimal place.",
     "Is the speed from Step 2 above or below the US highway speed limit of 65 mph? Answer 'above' or 'below'.",
     [str(round(25 * 3.6)), f"{round(25 * 3.6 * 0.6214, 1):.1f}", "below" if round(25 * 3.6 * 0.6214, 1) < 65 else "above"],
     "text", "medium"),
]
for (q1, q2, q3, answers, atype, diff) in conversion_chains:
    add_item(idx, [q1, q2, q3], answers, atype, diff)
    idx += 1

with open("_ccc_items.json", "w", encoding="utf-8") as f:
    json.dump(items, f, indent=2, ensure_ascii=False)
print(f"Wrote {len(items)} CCC items")
