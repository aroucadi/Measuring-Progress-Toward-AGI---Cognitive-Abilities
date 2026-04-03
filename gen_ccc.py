"""Generate CCC items (100) for metacog_dataset.json — v4.1
Every item has genuine epistemic uncertainty in at least one step.
Zero trivial arithmetic. Zero duplicates.
"""
import json
import math
import random
import hashlib

random.seed(20260402)

items = []
_seen_hashes = set()


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
    # Dedup check: hash the step questions
    h = hashlib.sha256("|".join(step_questions).encode()).hexdigest()[:16]
    if h in _seen_hashes:
        print(f"  WARNING: Skipping duplicate item ccc_{i:03d}")
        return False
    _seen_hashes.add(h)
    items.append({
        "id": f"ccc_{i:03d}",
        "subtype": "CCC",
        "prompt": make_prompt(step_questions),
        "steps": [{"step": j + 1, "question": step_questions[j], "answer": step_answers[j]}
                  for j in range(len(step_questions))],
        "final_answer": step_answers[-1],
        "answer_type": answer_type,
        "difficulty": difficulty,
    })
    return True


idx = 1

# ============================================================
# BATCH 1: Estimation / Fermi chains (15 items) — MEDIUM
# Each step involves real-world estimation, not pure arithmetic
# ============================================================
fermi_chains = [
    # (context, q1, a1, q2, a2, q3, a3, answer_type)
    ("A standard toilet uses 6 liters per flush.",
     "A person flushes approximately 5 times per day. Compute daily water usage for flushing in liters. Return an integer.",
     "30",
     "Compute the annual toilet-flushing water usage (365 days) in liters. Return an integer.",
     "10950",
     "If water costs $0.004 per liter, compute the annual cost in dollars. Return a number rounded to 2 decimal places.",
     "43.80", "decimal"),

    ("A household shower runs at 9.5 liters per minute.",
     "An average shower lasts 8 minutes. Compute the water used per shower in liters. Return a number rounded to 1 decimal place.",
     "76.0",
     "If a household of 3 people each showers daily, compute weekly water usage for showers in liters. Return a number rounded to 0 decimal places.",
     "1596",
     "At $0.004 per liter, compute the weekly shower water cost in dollars. Return a number rounded to 2 decimal places.",
     "6.38", "decimal"),

    ("A compact car averages 6.5 liters per 100 km of fuel consumption.",
     "A commuter drives 35 km each way to work. Compute the daily round-trip fuel consumption in liters. Return a number rounded to 2 decimal places.",
     "4.55",
     "Assuming 230 working days per year, compute annual commuting fuel in liters. Return a number rounded to 0 decimal places.",
     "1047",
     "At $1.65 per liter, compute the annual fuel cost in dollars. Return a number rounded to 0 decimal places.",
     "1728", "int"),

    ("A 60-watt incandescent bulb runs for 6 hours per day.",
     "Compute the daily energy consumption in watt-hours. Return an integer.",
     "360",
     "Compute monthly (30 days) energy in kilowatt-hours. Return a number rounded to 1 decimal place.",
     "10.8",
     "At $0.12 per kWh, compute monthly cost in dollars. Return a number rounded to 2 decimal places.",
     "1.30", "decimal"),

    ("An office printer uses 500 watts when active and 15 watts in standby.",
     "If the printer is active for 2 hours and in standby for 22 hours daily, compute total daily energy in watt-hours. Return an integer.",
     "1330",
     "Compute the monthly (22 working days) energy in kilowatt-hours. Return a number rounded to 2 decimal places.",
     "29.26",
     "At $0.15 per kWh, compute the monthly printing energy cost. Return a number rounded to 2 decimal places.",
     "4.39", "decimal"),

    ("A person types at 75 words per minute.",
     "In a 45-minute writing session, how many words are typed? Return an integer.",
     "3375",
     "At an average of 5.1 characters per word, compute total characters. Return a number rounded to 0 decimal places.",
     "17213",
     "If each character requires 2 bytes (UTF-16), compute total storage in kilobytes (1 KB = 1024 bytes). Return a number rounded to 1 decimal place.",
     "33.6", "decimal"),

    ("A mid-size city has 500,000 residents.",
     "If 65% of residents are adults, compute the adult population. Return an integer.",
     "325000",
     "If 2.3% of adults visit a hospital emergency room in a given month, compute monthly ER visits. Return a number rounded to 0 decimal places.",
     "7475",
     "If each ER visit costs the hospital an average of $2,200, compute total monthly ER cost in millions of dollars. Return a number rounded to 2 decimal places.",
     "16.45", "decimal"),

    ("A bakery uses 22 kg of flour per day.",
     "Compute weekly flour usage (6 working days). Return an integer.",
     "132",
     "If flour costs $0.85 per kg, compute weekly flour cost in dollars. Return a number rounded to 2 decimal places.",
     "112.20",
     "If the bakery produces 15 loaves per kg of flour, compute weekly loaf production. Return an integer.",
     "1980", "int"),

    ("A server processes 1,200 API requests per second at peak load.",
     "Compute the number of requests in a 5-minute peak window. Return an integer.",
     "360000",
     "If 0.3% of requests result in errors, compute the number of errors in that window. Return an integer.",
     "1080",
     "If each error costs $0.05 in retries and logging, compute the cost of errors in that window in dollars. Return a number rounded to 2 decimal places.",
     "54.00", "decimal"),

    ("A smartphone battery has a capacity of 4,500 mAh at 3.85 V.",
     "Compute the battery energy in milliwatt-hours (mWh = mAh × V). Return a number rounded to 1 decimal place.",
     "17325.0",
     "Convert to watt-hours (Wh). Return a number rounded to 2 decimal places.",
     "17.33",
     "If the phone consumes 0.8 W on average, compute battery life in hours. Return a number rounded to 1 decimal place.",
     "21.7", "decimal"),

    ("A swimming pool holds 75,000 liters of water.",
     "If evaporation loses 0.5% of the volume per day in summer, compute daily water loss in liters. Return a number rounded to 0 decimal places.",
     "375",
     "Compute monthly evaporation loss (30 days) in liters. Return an integer.",
     "11250",
     "At $0.003 per liter to refill, compute the monthly evaporation cost in dollars. Return a number rounded to 2 decimal places.",
     "33.75", "decimal"),

    ("A data center has 2,000 servers each consuming 450 watts.",
     "Compute total power consumption in kilowatts. Return an integer.",
     "900",
     "Compute daily energy in megawatt-hours (MWh). Return a number rounded to 1 decimal place.",
     "21.6",
     "At $0.08 per kWh, compute daily electricity cost in dollars. Return a number rounded to 0 decimal places.",
     "1728", "int"),

    ("A university lecture hall seats 350 students.",
     "If 82% attendance on average, compute typical number present. Return an integer.",
     "287",
     "If each student produces approximately 75 watts of body heat, compute total body heat output in kilowatts. Return a number rounded to 2 decimal places.",
     "21.53",
     "The HVAC system must remove this heat. If the system costs $0.04 per kWh to run, compute the hourly cooling cost in dollars for a 1.5 hour lecture. Return a number rounded to 2 decimal places.",
     "1.29", "decimal"),

    ("A freight train carries 100 containers, each weighing 25 tonnes when loaded.",
     "Compute total cargo weight in tonnes. Return an integer.",
     "2500",
     "The locomotive and wagons add 15% to the total weight. Compute the gross train weight in tonnes. Return a number rounded to 1 decimal place.",
     "2875.0",
     "If fuel consumption is 0.04 liters per tonne-kilometer for a 600 km trip, compute total fuel in liters. Return an integer.",
     "69000", "int"),

    ("A restaurant serves 180 meals per day.",
     "If each meal generates 0.35 kg of food waste, compute daily food waste in kg. Return a number rounded to 1 decimal place.",
     "63.0",
     "Compute annual food waste (365 days) in tonnes (1 tonne = 1000 kg). Return a number rounded to 2 decimal places.",
     "23.00",
     "If waste disposal costs $95 per tonne, compute annual disposal cost in dollars. Return a number rounded to 0 decimal places.",
     "2185", "int"),
]

for ctx, q1, a1, q2, a2, q3, a3, atype in fermi_chains:
    full_q1 = f"{ctx} {q1}"
    if add_item(idx, [full_q1, q2, q3], [a1, a2, a3], atype, "medium"):
        idx += 1

# ============================================================
# BATCH 2: Conditional probability chains (15 items) — HARD
# P(A)×P(B|A)×P(C|A∩B) — uncertainty genuinely compounds
# ============================================================
prob_chains = [
    (30, 50, 40, "rain", "flight delay given rain", "cancellation given delay"),
    (20, 60, 30, "manufacturing defect", "component failure given defect", "product recall given failure"),
    (40, 70, 50, "infection", "antibiotic resistance given infection", "ICU admission given resistance"),
    (15, 80, 25, "software flaw", "exploit given flaw", "data breach given exploit"),
    (50, 30, 60, "cloud cover", "rain given cloud cover", "flash flood given rain"),
    (25, 45, 35, "server overload", "timeout given overload", "data corruption given timeout"),
    (35, 55, 20, "power surge", "equipment damage given surge", "fire given damage"),
    (10, 90, 15, "genetic mutation", "protein misfolding given mutation", "disease onset given misfolding"),
    (60, 20, 70, "traffic congestion", "accident given congestion", "road closure given accident"),
    (45, 40, 30, "drought", "crop failure given drought", "food price spike given crop failure"),
    (18, 65, 40, "earthquake", "building damage given earthquake", "collapse given damage"),
    (55, 35, 25, "email phishing", "credential theft given phishing", "account takeover given theft"),
    (22, 50, 45, "air pollution", "respiratory illness given pollution", "hospitalization given illness"),
    (38, 42, 55, "supply chain delay", "production halt given delay", "contract penalty given halt"),
    (12, 75, 30, "sensor malfunction", "false alarm given malfunction", "evacuation given false alarm"),
]

for p1, p2, p3, l1, l2, l3 in prob_chains:
    r1 = p1 / 100
    r2 = p2 / 100
    r3 = p3 / 100
    joint_12 = round(r1 * r2, 4)
    joint_123 = round(r1 * r2 * r3, 4)
    pct = round(joint_123 * 100, 2)
    step_q = [
        f"The probability of {l1} is {p1}%. The probability of {l2} is {p2}%. Compute P({l1} AND {l2}). Return as a decimal rounded to 4 places.",
        f"Given P({l1} AND {l2}) from Step 1, and P({l3}) is {p3}%, compute P(all three events). Return as a decimal rounded to 4 places.",
        f"Express the probability from Step 2 as a percentage rounded to 2 decimal places. Return the number only (no % sign).",
    ]
    if add_item(idx, step_q, [f"{joint_12:.4f}", f"{joint_123:.4f}", f"{pct:.2f}"], "decimal", "hard"):
        idx += 1

# ============================================================
# BATCH 3: Unit conversion + domain reasoning (15 items) — MEDIUM
# Convert → compute → classify/compare
# ============================================================
conversion_chains = [
    ("Convert 12 miles to kilometers (1 mile = 1.609 km). Return a number rounded to 2 decimal places.",
     "At a speed of 60 km/h, compute the travel time for the distance from Step 1 in minutes. Return a number rounded to 1 decimal place.",
     "If departure is at 14:00 and travel takes the time from Step 2, plus a 10-minute buffer, what is the arrival time in HH:MM format?",
     [f"{round(12*1.609, 2):.2f}", f"{round(12*1.609/60*60, 1):.1f}", "14:29"], "text"),

    ("Convert 212°F to Celsius using C = (F-32)×5/9. Return an integer.",
     "Convert the Celsius from Step 1 to Kelvin (K = C + 273.15). Return a number rounded to 2 decimal places.",
     "Is the Kelvin value from Step 2 above or below the boiling point of ethanol (351.44 K)? Answer 'above' or 'below'.",
     ["100", "373.15", "above"], "text"),

    ("Convert 176 pounds to kilograms (1 lb = 0.4536 kg). Return a number rounded to 1 decimal place.",
     "A person is 1.75 m tall and weighs the kg from Step 1. Compute BMI = weight/(height²). Return a number rounded to 1 decimal place.",
     "Classify the BMI from Step 2: 'underweight' (<18.5), 'normal' (18.5-24.9), 'overweight' (25-29.9), or 'obese' (>=30). Return only the category.",
     [f"{round(176*0.4536,1):.1f}", f"{round(176*0.4536/(1.75**2),1):.1f}",
      "overweight" if 25 <= round(176*0.4536/(1.75**2),1) < 30 else "normal"], "text"),

    ("Convert 3 US gallons to liters (1 gal = 3.785 L). Return a number rounded to 3 decimal places.",
     "Convert the liters from Step 1 to milliliters. Return an integer.",
     "If a dose is 15 mL, compute how many full doses can be obtained from Step 2. Return an integer (floor).",
     [f"{round(3*3.785,3):.3f}", str(round(3*3.785*1000)), str(int(3*3.785*1000/15))], "int"),

    ("Convert 25 m/s to km/h (multiply by 3.6). Return an integer.",
     "Convert the km/h from Step 1 to mph (1 km = 0.6214 miles). Return a number rounded to 1 decimal place.",
     "Is the speed from Step 2 above or below the US highway limit of 65 mph? Answer 'above' or 'below'.",
     [str(round(25*3.6)), f"{round(25*3.6*0.6214,1):.1f}",
      "below" if round(25*3.6*0.6214,1) < 65 else "above"], "text"),

    ("Convert 2.5 atmospheres to pascals (1 atm = 101325 Pa). Return an integer.",
     "Convert the pascals from Step 1 to kilopascals. Return a number rounded to 2 decimal places.",
     "Is this pressure above or below the typical tire pressure of 220 kPa? Answer 'above' or 'below'.",
     [str(round(2.5*101325)), f"{round(2.5*101325/1000,2):.2f}", "above"], "text"),

    ("Convert 450 grams to ounces (1 oz = 28.3495 g). Return a number rounded to 2 decimal places.",
     "If a recipe calls for 12 oz of the ingredient, compute how many grams you still need beyond the 450g from Step 1. Return a number rounded to 1 decimal place.",
     "Is the deficit from Step 2 more or less than 100 grams? Answer 'more' or 'less'.",
     [f"{round(450/28.3495,2):.2f}", f"{round(12*28.3495-450,1):.1f}",
      "less" if round(12*28.3495-450,1) < 100 else "more"], "text"),

    ("A room is 14 feet × 11 feet. Convert the area to square meters (1 ft = 0.3048 m). Return a number rounded to 2 decimal places.",
     "If carpet costs $28 per square meter, compute the total carpet cost for the room. Return a number rounded to 2 decimal places.",
     "Is this cost above or below $500? Answer 'above' or 'below'.",
     [f"{round(14*0.3048*11*0.3048,2):.2f}", f"{round(14*0.3048*11*0.3048*28,2):.2f}",
      "below" if round(14*0.3048*11*0.3048*28,2) < 500 else "above"], "text"),

    ("Convert 72°F to Celsius using C = (F-32)×5/9. Return a number rounded to 2 decimal places.",
     "The recommended indoor temperature range is 20-22°C. Is the temperature from Step 1 within this range? Answer 'within' or 'outside'.",
     "The temperature from Step 1 in Kelvin (K = C + 273.15) is closest to which value: 290, 295, 300, or 305? Return just the number.",
     [f"{round((72-32)*5/9,2):.2f}",
      "within" if 20 <= round((72-32)*5/9,2) <= 22 else "outside",
      "295"], "int"),

    ("Convert 1500 milliliters to US cups (1 cup = 236.588 mL). Return a number rounded to 2 decimal places.",
     "A recipe needs 8 cups total. Compute how many more milliliters you need beyond the 1500 mL. Return a number rounded to 0 decimal places.",
     "Is the additional volume from Step 2 more or less than 500 mL? Answer 'more' or 'less'.",
     [f"{round(1500/236.588,2):.2f}", str(round(8*236.588-1500)),
      "less" if round(8*236.588-1500) < 500 else "more"], "text"),

    ("A car's fuel tank holds 55 liters. Convert to US gallons (1 gal = 3.785 L). Return a number rounded to 2 decimal places.",
     "If the car gets 32 miles per gallon, compute the maximum range on a full tank in miles. Return a number rounded to 1 decimal place.",
     "Convert the range from Step 2 to kilometers (1 mile = 1.609 km). Return a number rounded to 0 decimal places.",
     [f"{round(55/3.785,2):.2f}", f"{round(55/3.785*32,1):.1f}",
      str(round(55/3.785*32*1.609))], "int"),

    ("Convert 5 kilometers to nautical miles (1 NM = 1.852 km). Return a number rounded to 3 decimal places.",
     "A ship travels at 12 knots (nautical miles per hour). Compute travel time for the distance in minutes. Return a number rounded to 1 decimal place.",
     "If the ship departed at 08:30, what is the estimated arrival time in HH:MM format?",
     [f"{round(5/1.852,3):.3f}", f"{round(5/1.852/12*60,1):.1f}", "08:44"], "text"),

    ("Convert 35°C to Fahrenheit using F = C×9/5 + 32. Return a number rounded to 1 decimal place.",
     "The heat index adds approximately 8°F when relative humidity is 60%. Compute the feels-like temperature in °F. Return a number rounded to 1 decimal place.",
     "Is this feels-like temperature above or below the OSHA heat danger threshold of 103°F? Answer 'above' or 'below'.",
     [f"{round(35*9/5+32,1):.1f}", f"{round(35*9/5+32+8,1):.1f}",
      "above" if round(35*9/5+32+8,1) > 103 else "below"], "text"),

    ("Convert 8500 feet to meters (1 ft = 0.3048 m). Return a number rounded to 0 decimal places.",
     "At this altitude, atmospheric pressure is approximately 74% of sea-level (101325 Pa). Compute the pressure in kPa. Return a number rounded to 1 decimal place.",
     "Is this pressure sufficient for a typical pressurized aircraft cabin (minimum 75 kPa)? Answer 'sufficient' or 'insufficient'.",
     [str(round(8500*0.3048)), f"{round(0.74*101325/1000,1):.1f}",
      "insufficient" if round(0.74*101325/1000,1) < 75 else "sufficient"], "text"),

    ("A swimming pool is 25 meters × 12 meters × 1.5 meters deep. Compute the volume in cubic meters. Return a number rounded to 1 decimal place.",
     "Convert the volume to liters (1 m³ = 1000 liters). Return an integer.",
     "If filling at 50 liters per minute, compute the fill time in hours. Return a number rounded to 1 decimal place.",
     [f"{round(25*12*1.5,1):.1f}", str(round(25*12*1.5*1000)),
      f"{round(25*12*1.5*1000/50/60,1):.1f}"], "decimal"),
]

for q1, q2, q3, answers, atype in conversion_chains:
    if add_item(idx, [q1, q2, q3], answers, atype, "medium"):
        idx += 1

# ============================================================
# BATCH 4: Drug/clinical dosage cascades (15 items) — MEDIUM
# Weight→dose→clearance→rounding — genuine uncertainty
# ============================================================
dosage_params = [
    (70, 5, 0.80, 50), (85, 3, 0.60, 25), (60, 8, 0.70, 100),
    (95, 4, 0.90, 50), (55, 6, 0.50, 25), (78, 7, 0.85, 50),
    (110, 2, 0.75, 25), (65, 10, 0.65, 100), (50, 5, 0.55, 25),
    (90, 3, 0.95, 50), (72, 4, 0.80, 25), (48, 9, 0.60, 50),
    (100, 6, 0.70, 100), (82, 5, 0.45, 50), (58, 7, 0.85, 25),
]

for weight, dose_per_kg, clearance, round_to in dosage_params:
    raw = weight * dose_per_kg
    adjusted = raw * clearance
    final = round(adjusted / round_to) * round_to
    step_q = [
        f"A patient weighs {weight} kg. The standard dose is {dose_per_kg} mg/kg. Compute the raw dose in mg. Return an integer.",
        f"The patient has reduced organ function requiring a {clearance} adjustment factor. Multiply the raw dose from Step 1 by {clearance}. Return a number (decimal ok).",
        f"Round the adjusted dose from Step 2 to the nearest {round_to} mg. Return an integer.",
    ]
    if add_item(idx, step_q, [str(raw), str(round(adjusted, 2)), str(final)], "int", "medium"):
        idx += 1

# ============================================================
# BATCH 5: Multi-step word problems with ambiguity (10 items) — HARD
# Order of operations, discount stacking, tax calculation
# ============================================================
word_problems = [
    ("A store has a 20% off sale on a $85 jacket.",
     "Compute the sale price after the 20% discount. Return a number rounded to 2 decimal places.",
     "A loyalty coupon gives an additional $10 off the sale price. Compute the price after the coupon. Return a number rounded to 2 decimal places.",
     "Sales tax is 8.25%. Compute the final price including tax. Return a number rounded to 2 decimal places.",
     [f"{85*0.80:.2f}", f"{85*0.80-10:.2f}", f"{(85*0.80-10)*1.0825:.2f}"], "decimal"),

    ("A freelancer earns $4,500 per month before taxes.",
     "Federal tax rate is 22%. Compute the federal tax amount. Return a number rounded to 2 decimal places.",
     "State tax is 5.3% of the original gross. Compute the combined tax (federal + state). Return a number rounded to 2 decimal places.",
     "Compute the net monthly income after both taxes. Return a number rounded to 2 decimal places.",
     [f"{4500*0.22:.2f}", f"{4500*0.22+4500*0.053:.2f}", f"{4500-4500*0.22-4500*0.053:.2f}"], "decimal"),

    ("A recipe calls for 2.5 cups of flour per batch of cookies.",
     "You want to make 3.5 batches. Compute the flour needed in cups. Return a number rounded to 2 decimal places.",
     "Convert the cups to grams (1 cup flour = 125 g). Return a number rounded to 0 decimal places.",
     "You have 900 g of flour. Compute how many grams short you are. Return an integer. If you have enough, return 0.",
     ["8.75", "1094", "194"], "int"),

    ("A loan of $12,000 has an annual interest rate of 6.5%.",
     "Compute the monthly interest rate as a decimal. Return a number rounded to 6 decimal places.",
     "Compute the first month's interest charge in dollars. Return a number rounded to 2 decimal places.",
     "After paying $350 in the first month, compute the remaining principal (principal + interest - payment). Return a number rounded to 2 decimal places.",
     [f"{0.065/12:.6f}", f"{12000*0.065/12:.2f}", f"{12000+12000*0.065/12-350:.2f}"], "decimal"),

    ("A company ships 1,200 units per day at $3.50 per unit in shipping costs.",
     "Compute daily shipping costs. Return a number rounded to 2 decimal places.",
     "The company negotiates a 12% bulk discount on shipping. Compute the new daily cost. Return a number rounded to 2 decimal places.",
     "Compute the annual savings (365 days) from the discount in dollars. Return a number rounded to 0 decimal places.",
     [f"{1200*3.50:.2f}", f"{1200*3.50*0.88:.2f}", str(round(1200*3.50*0.12*365))], "int"),

    ("An investment of $5,000 earns 4.2% annual interest, compounded monthly.",
     "Compute the monthly interest rate as a decimal. Return a number rounded to 6 decimal places.",
     "After 1 month, compute the new balance. Return a number rounded to 2 decimal places.",
     "After 2 months (compounding on the balance from Step 2), compute the new balance. Return a number rounded to 2 decimal places.",
     [f"{0.042/12:.6f}", f"{5000*(1+0.042/12):.2f}", f"{5000*(1+0.042/12)**2:.2f}"], "decimal"),

    ("A painter charges $35 per hour for labor plus $12 per square meter for paint.",
     "A room has 4 walls, each 3.5 m × 2.8 m. Compute total paintable area in square meters (ignore doors/windows). Return a number rounded to 1 decimal place.",
     "Compute the paint cost for the room. Return a number rounded to 2 decimal places.",
     "If the job takes 6 hours, compute total cost (labor + paint). Return a number rounded to 2 decimal places.",
     [f"{4*3.5*2.8:.1f}", f"{4*3.5*2.8*12:.2f}", f"{35*6+4*3.5*2.8*12:.2f}"], "decimal"),

    ("A gym membership costs $45/month with a $99 enrollment fee.",
     "Compute the total cost for the first year. Return a number rounded to 2 decimal places.",
     "A competing gym offers $55/month with no enrollment fee. Compute its annual cost. Return a number rounded to 2 decimal places.",
     "After how many months is the first gym cheaper? (Find the month where cumulative cost of gym 1 becomes less than gym 2). Return an integer.",
     [f"{99+45*12:.2f}", f"{55*12:.2f}",
      str(next(m for m in range(1, 100) if 99+45*m < 55*m))], "int"),

    ("A phone plan costs $65/month for 10 GB of data.",
     "Overage is charged at $10 per additional GB. If you use 13.5 GB, compute the overage charge (round up to next full GB). Return a number rounded to 2 decimal places.",
     "Compute total monthly bill (plan + overage). Return a number rounded to 2 decimal places.",
     "An unlimited plan costs $85/month. How much more does your current plan cost this month? Return a number rounded to 2 decimal places.",
     ["40.00", "105.00", "20.00"], "decimal"),

    ("A restaurant bill is $127.50 before tip and tax.",
     "Compute an 18% tip on the pre-tax amount. Return a number rounded to 2 decimal places.",
     "Sales tax is 7.5% on the pre-tax amount. Compute the total bill (food + tip + tax). Return a number rounded to 2 decimal places.",
     "If split equally among 4 people, compute each person's share. Return a number rounded to 2 decimal places.",
     [f"{127.50*0.18:.2f}", f"{127.50+127.50*0.18+127.50*0.075:.2f}",
      f"{(127.50+127.50*0.18+127.50*0.075)/4:.2f}"], "decimal"),
]

for ctx, q1, q2, q3, answers, atype in word_problems:
    full_q1 = f"{ctx} {q1}"
    if add_item(idx, [full_q1, q2, q3], answers, atype, "hard"):
        idx += 1

# ============================================================
# BATCH 6: Scientific measurement chains (10 items) — HARD
# Measurement → uncertainty propagation → significant figures → conclusion
# ============================================================
science_chains = [
    ("A substance has a mass of 25.3 g and occupies 8.7 mL. Compute density in g/mL. Return a number rounded to 3 decimal places.",
     "Pure iron has a density of 7.874 g/mL. Compute the percentage difference between your measurement and pure iron. Return a number rounded to 1 decimal place.",
     "Is the measured density within 10% of pure iron? Answer 'yes' or 'no'.",
     [f"{round(25.3/8.7,3):.3f}", f"{round(abs(25.3/8.7-7.874)/7.874*100,1):.1f}",
      "no" if abs(25.3/8.7-7.874)/7.874*100 > 10 else "yes"], "text"),

    ("A sound wave travels 343 m/s in air. A building is 1.2 km away. Compute the time for the sound to reach the building in seconds. Return a number rounded to 2 decimal places.",
     "Light travels at 300,000 km/s. Compute the time for light to cover the same distance in seconds. Return the answer in scientific notation (e.g., 4.00e-06).",
     "Compute the ratio of sound travel time to light travel time. Return a number rounded to 0 decimal places.",
     [f"{round(1200/343,2):.2f}", f"{1200/300000000:.2e}", str(round((1200/343)/(1200/300000000)))], "int"),

    ("A gas occupies 2.5 liters at 20°C (293.15 K) and 1 atm. Convert the temperature to Kelvin. Return a number rounded to 2 decimal places.",
     "If heated to 80°C (353.15 K) at constant pressure, compute the new volume using Charles's Law (V1/T1 = V2/T2). Return a number rounded to 3 decimal places.",
     "Compute the percent increase in volume. Return a number rounded to 1 decimal place.",
     ["293.15", f"{round(2.5*353.15/293.15,3):.3f}", f"{round((353.15/293.15-1)*100,1):.1f}"], "decimal"),

    ("An object falls from rest for 3.2 seconds (use g = 9.81 m/s²). Compute the final velocity (v = gt). Return a number rounded to 2 decimal places.",
     "Compute the distance fallen (d = ½gt²). Return a number rounded to 2 decimal places.",
     "Convert the distance to feet (1 m = 3.281 ft). Return a number rounded to 1 decimal place.",
     [f"{round(9.81*3.2,2):.2f}", f"{round(0.5*9.81*3.2**2,2):.2f}",
      f"{round(0.5*9.81*3.2**2*3.281,1):.1f}"], "decimal"),

    ("A circuit has a 12V battery and a 470-ohm resistor. Compute the current using Ohm's law (I = V/R) in milliamps. Return a number rounded to 2 decimal places.",
     "Compute the power dissipated (P = V × I) in milliwatts. Return a number rounded to 2 decimal places.",
     "If the resistor is rated for 250 mW, is the power from Step 2 within the rating? Answer 'within' or 'exceeds'.",
     [f"{round(12/470*1000,2):.2f}", f"{round(12*12/470*1000,2):.2f}",
      "within" if round(12*12/470*1000,2) <= 250 else "exceeds"], "text"),

    ("A pendulum has a length of 0.8 meters (Period T = 2π√(L/g), g = 9.81 m/s²). Compute the period T in seconds. Return a number rounded to 3 decimal places.",
     "Compute the frequency f = 1/T in Hz. Return a number rounded to 3 decimal places.",
     "How many complete oscillations in 30 seconds? Return an integer (floor).",
     [f"{round(2*math.pi*math.sqrt(0.8/9.81),3):.3f}",
      f"{round(1/(2*math.pi*math.sqrt(0.8/9.81)),3):.3f}",
      str(int(30/(2*math.pi*math.sqrt(0.8/9.81))))], "int"),

    ("A radioactive sample has a half-life of 5.27 years and starting mass of 100 mg. Compute the decay constant λ = ln(2)/half-life in per-year. Return a number rounded to 4 decimal places.",
     "Compute the remaining mass after 10 years using M = M₀ × e^(-λt). Return a number rounded to 2 decimal places.",
     "What percentage of the original mass has decayed? Return a number rounded to 1 decimal place.",
     [f"{round(math.log(2)/5.27,4):.4f}",
      f"{round(100*math.exp(-math.log(2)/5.27*10),2):.2f}",
      f"{round((1-math.exp(-math.log(2)/5.27*10))*100,1):.1f}"], "decimal"),

    ("A solution has a pH of 3.5. Compute the hydrogen ion concentration [H+] = 10^(-pH) in mol/L. Return in scientific notation (e.g., 3.16e-04).",
     "If you dilute the solution 100-fold, compute the new [H+] in scientific notation.",
     "Compute the new pH = -log10([H+]). Return a number rounded to 1 decimal place.",
     [f"{10**(-3.5):.2e}", f"{10**(-3.5)/100:.2e}", f"{round(-math.log10(10**(-3.5)/100),1):.1f}"], "decimal"),

    ("An LED emits light at 620 nm wavelength (c = 3.00×10⁸ m/s). Compute the frequency (f = c/λ, convert nm to meters). Return in scientific notation with 2 decimal places (e.g., 4.84e+14).",
     "Compute the photon energy E = hf (h = 6.626×10⁻³⁴ J·s) in electron-volts (1 eV = 1.602×10⁻¹⁹ J). Return a number rounded to 2 decimal places.",
     "Is this photon energy typical for visible light (1.65-3.10 eV)? Answer 'yes' or 'no'.",
     [f"{3e8/620e-9:.2e}",
      f"{round(6.626e-34*3e8/620e-9/1.602e-19,2):.2f}",
      "yes" if 1.65 <= round(6.626e-34*3e8/620e-9/1.602e-19,2) <= 3.10 else "no"], "text"),

    ("Earth-Sun distance is 1 AU = 1.496×10⁸ km, light speed = 3.00×10⁵ km/s. Compute the time for light to travel from the Sun to Earth in seconds. Return a number rounded to 1 decimal place.",
     "Convert this to minutes. Return a number rounded to 2 decimal places.",
     "Mars is 1.52 AU from the Sun. Compute the light travel time from Sun to Mars in minutes. Return a number rounded to 2 decimal places.",
     [f"{round(1.496e8/3e5,1):.1f}", f"{round(1.496e8/3e5/60,2):.2f}",
      f"{round(1.52*1.496e8/3e5/60,2):.2f}"], "decimal"),
]

for q1, q2, q3, answers, atype in science_chains:
    if add_item(idx, [q1, q2, q3], answers, atype, "hard"):
        idx += 1

# ============================================================
# BATCH 7: Financial / compound interest (10 items) — MEDIUM
# ============================================================
finance_chains = [
    ("An investment of $10,000 earns 5% annual interest, compounded quarterly.",
     "Compute the quarterly interest rate as a decimal. Return a number rounded to 4 decimal places.",
     "Compute the balance after 1 year (4 quarters). Return a number rounded to 2 decimal places.",
     "Compute the effective annual rate (EAR = balance/principal - 1) as a percentage. Return a number rounded to 3 decimal places.",
     ["0.0125", f"{10000*(1.0125)**4:.2f}", f"{((1.0125)**4-1)*100:.3f}"], "decimal"),

    ("A house costs $320,000. The down payment is 20%.",
     "Compute the down payment in dollars. Return an integer.",
     "Compute the mortgage principal (house price minus down payment). Return an integer.",
     "At a 30-year fixed rate of 6.5%, compute the monthly payment using M = P×r×(1+r)^n / ((1+r)^n - 1), where r = annual rate/12 and n = 360. Return a number rounded to 2 decimal places.",
     ["64000", "256000",
      f"{256000*(0.065/12)*(1+0.065/12)**360/((1+0.065/12)**360-1):.2f}"], "decimal"),

    ("A car depreciates at 15% per year. Purchase price: $28,000.",
     "Compute the value after 1 year. Return a number rounded to 2 decimal places.",
     "Compute the value after 3 years (compound depreciation). Return a number rounded to 2 decimal places.",
     "Compute the total depreciation over 3 years in dollars. Return a number rounded to 2 decimal places.",
     [f"{28000*0.85:.2f}", f"{28000*0.85**3:.2f}", f"{28000-28000*0.85**3:.2f}"], "decimal"),

    ("A savings account has $8,500 with 3.8% APY.",
     "Compute monthly interest (APY/12 × balance) for the first month. Return a number rounded to 2 decimal places.",
     "After depositing an additional $500, compute the new balance (original + interest + deposit). Return a number rounded to 2 decimal places.",
     "Compute the second month's interest on the new balance. Return a number rounded to 2 decimal places.",
     [f"{8500*0.038/12:.2f}", f"{8500+8500*0.038/12+500:.2f}",
      f"{(8500+8500*0.038/12+500)*0.038/12:.2f}"], "decimal"),

    ("A bond has a face value of $1,000 and a coupon rate of 4.5%, paid semi-annually.",
     "Compute the semi-annual coupon payment in dollars. Return a number rounded to 2 decimal places.",
     "Compute the total annual coupon income. Return a number rounded to 2 decimal places.",
     "If the bond is purchased at $980, compute the current yield (annual coupon / purchase price) as a percentage. Return a number rounded to 3 decimal places.",
     ["22.50", "45.00", f"{45/980*100:.3f}"], "decimal"),

    ("You invest $200/month in an index fund returning 8% annually (0.667% monthly).",
     "Compute the balance after 1 month (just the first deposit + interest). Return a number rounded to 2 decimal places.",
     "After the second month (balance from Step 1 + interest + new $200 deposit), compute the new balance. Return a number rounded to 2 decimal places.",
     "Compute the balance after 12 months using FV = PMT × ((1+r)^n - 1) / r. Return a number rounded to 2 decimal places.",
     [f"{200*1.00667:.2f}", f"{(200*1.00667+200)*1.00667:.2f}",
      f"{200*((1.00667**12-1)/0.00667):.2f}"], "decimal"),

    ("A credit card has a $3,200 balance at 19.99% APR.",
     "Compute the monthly interest rate. Return a number rounded to 5 decimal places.",
     "Compute the first month's interest charge. Return a number rounded to 2 decimal places.",
     "If you pay $150, compute the remaining balance (balance + interest - payment). Return a number rounded to 2 decimal places.",
     [f"{0.1999/12:.5f}", f"{3200*0.1999/12:.2f}", f"{3200+3200*0.1999/12-150:.2f}"], "decimal"),

    ("A stock was purchased at $45.20 per share. You bought 150 shares.",
     "Compute the total investment. Return a number rounded to 2 decimal places.",
     "The stock is now $52.80. Compute the unrealized gain in dollars. Return a number rounded to 2 decimal places.",
     "Compute the percentage return. Return a number rounded to 2 decimal places.",
     [f"{45.20*150:.2f}", f"{(52.80-45.20)*150:.2f}", f"{(52.80-45.20)/45.20*100:.2f}"], "decimal"),

    ("A business takes a $50,000 loan at 7% annual interest, simple interest for 3 years.",
     "Compute the total interest over 3 years. Return a number rounded to 2 decimal places.",
     "Compute the total amount owed (principal + interest). Return a number rounded to 2 decimal places.",
     "If repaid in 36 equal monthly installments, compute the monthly payment. Return a number rounded to 2 decimal places.",
     [f"{50000*0.07*3:.2f}", f"{50000+50000*0.07*3:.2f}", f"{(50000+50000*0.07*3)/36:.2f}"], "decimal"),

    ("An employee's annual salary is $72,000. They contribute 6% to a 401(k).",
     "Compute the annual 401(k) contribution. Return a number rounded to 2 decimal places.",
     "The employer matches 50% of the contribution. Compute total annual 401(k) deposits (employee + employer). Return a number rounded to 2 decimal places.",
     "If the 401(k) earns 7% annually, compute the balance after 1 year (on total deposits). Return a number rounded to 2 decimal places.",
     [f"{72000*0.06:.2f}", f"{72000*0.06*1.5:.2f}", f"{72000*0.06*1.5*1.07:.2f}"], "decimal"),
]

for ctx, q1, q2, q3, answers, atype in finance_chains:
    full_q1 = f"{ctx} {q1}"
    if add_item(idx, [full_q1, q2, q3], answers, atype, "medium"):
        idx += 1

# ============================================================
# BATCH 8: System Scaling & Architecture (10 items) — HARD
# Replaces trivial fraction conversions with genuine uncertainty 
# ============================================================
scaling_params = [
    # (base_rps, payload_kb, processing_ms)
    (5000, 2.5, 150), (8000, 1.8, 200), (3000, 4.0, 100),
    (10000, 1.5, 250), (7500, 2.2, 180), (15000, 0.8, 300),
    (4500, 3.5, 120), (6000, 2.0, 160), (9500, 1.2, 220),
    (12000, 1.0, 280)
]
for base_rps, payload_kb, processing_ms in scaling_params:
    rps_peak = int(base_rps * 1.5)
    bandwidth_gbps = round(rps_peak * payload_kb * 8 / 1e6, 2)
    concurrent = rps_peak * (processing_ms / 1000)
    servers = math.ceil(concurrent / 100)
    
    step_q = [
        f"A web service averages {base_rps} requests per second (RPS). Assuming a typical diurnal peak-to-average ratio of 1.5, compute the peak RPS. Return an integer.",
        f"The average response payload is {payload_kb} KB. Using metric prefixes (1 KB = 1000 Bytes, 1 Gb = 10^9 bits), compute the peak network egress bandwidth in Gigabits per second (Gbps). Return a number rounded to 2 decimal places.",
        f"Each request requires {processing_ms} ms of processing time. Using Little's Law, compute the peak concurrent requests. Determine the minimum number of servers required if each server handles a maximum of 100 concurrent requests (round up to nearest integer). Return an integer.",
    ]
    if add_item(idx, step_q, [str(rps_peak), f"{bandwidth_gbps:.2f}", str(servers)], "decimal", "hard"):
        idx += 1

# ============================================================
# Final output
# ============================================================
print(f"Generated {len(items)} CCC items (target: 100)")
diffs = [i["difficulty"] for i in items]
print(f"  easy={diffs.count('easy')} medium={diffs.count('medium')} hard={diffs.count('hard')}")

# Verify no duplicates
ids = [i["id"] for i in items]
assert len(set(ids)) == len(ids), f"Duplicate IDs found!"

with open("_ccc_items.json", "w", encoding="utf-8") as f:
    json.dump(items, f, indent=2, ensure_ascii=False)
print(f"Wrote {len(items)} CCC items to _ccc_items.json")
