"""Generate CR items (80) for metacog_dataset.json — v4.1
5 diverse error types: factual, logical, unit/dimensional, statistical, definitional.
Error position varies (L1, L2, or L3) — no predictable pattern.
Each item includes accepted_corrections for flexible scoring.
"""
import json
import random

random.seed(20260402)

items = []


def add_item(i: int, prompt: str, error_location: str, correction: str,
             accepted_corrections: list[str], difficulty: str, error_type: str):
    items.append({
        "id": f"cr_{i:03d}",
        "subtype": "CR",
        "prompt": prompt,
        "error_location": error_location,
        "correction": correction,
        "accepted_corrections": accepted_corrections,
        "difficulty": difficulty,
        "error_type": error_type,
    })


def make_header(task: str) -> str:
    return (
        "You are reviewing a short reasoning transcript that contains exactly ONE error.\n"
        "Your job is to locate the error and provide the correction.\n"
        "Output a SINGLE JSON object on the last line with keys: error_location, correction.\n"
        "error_location must be one of the line labels like \"L3\".\n\n"
        f"Task: {task}\n\n"
    )


idx = 1

# ============================================================
# TYPE 1: Factual/historical errors (16 items) — Error in dates, names, places
# ============================================================
factual_errors = [
    # (task_desc, lines[], error_line, correction, accepted, difficulty)
    ("Verify the following historical account.",
     ["[L1] The Declaration of Independence was adopted on July 4, 1776.",
      "[L2] It was primarily authored by Benjamin Franklin.",
      "[L3] The document declared the thirteen colonies free from British rule."],
     "L2", "The Declaration of Independence was primarily authored by Thomas Jefferson.",
     ["Thomas Jefferson", "authored by Thomas Jefferson", "Jefferson"], "easy"),

    ("Check this account of World War I.",
     ["[L1] World War I began in 1914 following the assassination of Archduke Franz Ferdinand.",
      "[L2] The war ended with the Treaty of Versailles, signed in 1920.",
      "[L3] The treaty imposed heavy reparations on Germany."],
     "L2", "The Treaty of Versailles was signed on June 28, 1919.",
     ["1919", "signed in 1919", "June 28, 1919"], "easy"),

    ("Verify these facts about the solar system.",
     ["[L1] Jupiter is the largest planet in our solar system.",
      "[L2] Saturn is known for its prominent ring system.",
      "[L3] Mars is the closest planet to the Sun."],
     "L3", "Mercury is the closest planet to the Sun.",
     ["Mercury", "Mercury is the closest planet to the Sun"], "easy"),

    ("Check this description of human anatomy.",
     ["[L1] The human body has 206 bones in adulthood.",
      "[L2] The femur, located in the upper arm, is the longest bone.",
      "[L3] Red blood cells are produced in bone marrow."],
     "L2", "The femur is located in the upper leg (thigh), not the upper arm.",
     ["upper leg", "thigh", "femur is in the thigh", "femur is located in the upper leg"], "easy"),

    ("Verify this description of the water cycle.",
     ["[L1] Water evaporates from oceans, lakes, and rivers due to solar energy.",
      "[L2] Water vapor rises and cools, forming clouds through condensation.",
      "[L3] Precipitation falls as rain, snow, or sleet, returning water to the ground.",
      "[L4] Groundwater flows directly into the stratosphere to restart the cycle."],
     "L4", "Groundwater flows into rivers, lakes, and oceans (not the stratosphere) to restart the cycle.",
     ["rivers", "oceans", "not the stratosphere", "groundwater flows into bodies of water"], "medium"),

    ("Check these facts about chemical elements.",
     ["[L1] Gold has the chemical symbol Au and atomic number 79.",
      "[L2] Oxygen makes up approximately 21% of Earth's atmosphere.",
      "[L3] The lightest element is helium, with an atomic number of 2."],
     "L3", "The lightest element is hydrogen (atomic number 1), not helium.",
     ["hydrogen", "hydrogen is the lightest", "atomic number 1"], "medium"),

    ("Verify this account of the moon landing.",
     ["[L1] NASA's Apollo 11 mission launched on July 16, 1969.",
      "[L2] Buzz Aldrin was the first person to walk on the Moon.",
      "[L3] The mission safely returned to Earth on July 24, 1969."],
     "L2", "Neil Armstrong was the first person to walk on the Moon, not Buzz Aldrin.",
     ["Neil Armstrong", "Armstrong was the first", "Neil Armstrong was first"], "easy"),

    ("Check this geography description.",
     ["[L1] The Nile is the longest river in Africa.",
      "[L2] Mount Kilimanjaro, the highest peak in Africa, is located in Kenya.",
      "[L3] The Sahara is the largest hot desert in the world."],
     "L2", "Mount Kilimanjaro is located in Tanzania, not Kenya.",
     ["Tanzania", "located in Tanzania"], "medium"),

    ("Verify these facts about the periodic table.",
     ["[L1] The noble gases are in Group 18 and include helium, neon, and argon.",
      "[L2] Sodium (Na) and potassium (K) are alkaline earth metals in Group 2.",
      "[L3] Carbon has four valence electrons and forms the basis of organic chemistry."],
     "L2", "Sodium and potassium are alkali metals in Group 1, not alkaline earth metals in Group 2.",
     ["alkali metals", "Group 1", "alkali metals in Group 1"], "medium"),

    ("Check this account of computer science history.",
     ["[L1] Alan Turing proposed the concept of a universal computing machine in 1936.",
      "[L2] The first electronic general-purpose computer, ENIAC, was completed in 1945.",
      "[L3] Tim Berners-Lee invented the Internet in 1989."],
     "L3", "Tim Berners-Lee invented the World Wide Web (not the Internet) in 1989. The Internet predates it.",
     ["World Wide Web", "WWW", "the Web, not the Internet"], "medium"),

    ("Verify this biological classification.",
     ["[L1] Dolphins are fish that live in oceans and occasionally in rivers.",
      "[L2] They use echolocation to navigate and find prey.",
      "[L3] Dolphins are highly social and live in groups called pods."],
     "L1", "Dolphins are mammals, not fish. They are marine mammals of the order Cetacea.",
     ["mammals", "dolphins are mammals", "marine mammals"], "easy"),

    ("Check this physics description.",
     ["[L1] The speed of light in a vacuum is approximately 3 × 10⁸ m/s.",
      "[L2] Sound travels faster than light in all media.",
      "[L3] Light exhibits both wave and particle properties (wave-particle duality)."],
     "L2", "Light travels faster than sound in all media, not the reverse.",
     ["light travels faster than sound", "light is faster", "sound is slower than light"], "easy"),

    ("Verify this economic history.",
     ["[L1] The Great Depression began with the stock market crash of October 1929.",
      "[L2] The depression lasted through most of the 1930s.",
      "[L3] The New Deal was introduced by President Herbert Hoover to combat the crisis."],
     "L3", "The New Deal was introduced by President Franklin D. Roosevelt, not Herbert Hoover.",
     ["Franklin D. Roosevelt", "FDR", "Roosevelt"], "easy"),

    ("Check these statements about DNA.",
     ["[L1] DNA stands for deoxyribonucleic acid.",
      "[L2] The double helix structure of DNA was discovered by Watson and Crick in 1953.",
      "[L3] DNA contains five base types: adenine, thymine, guanine, cytosine, and uracil."],
     "L3", "DNA contains four bases: adenine, thymine, guanine, and cytosine. Uracil is found in RNA, not DNA.",
     ["four bases", "uracil is in RNA", "DNA has four bases, not five"], "medium"),

    ("Verify this description of photosynthesis.",
     ["[L1] Photosynthesis occurs primarily in the mitochondria of plant cells.",
      "[L2] It converts carbon dioxide and water into glucose and oxygen.",
      "[L3] Light energy from the Sun drives the process."],
     "L1", "Photosynthesis occurs in the chloroplasts, not the mitochondria.",
     ["chloroplasts", "occurs in chloroplasts", "chloroplast"], "easy"),

    ("Check this music history statement.",
     ["[L1] Ludwig van Beethoven was a German composer born in 1770.",
      "[L2] He composed nine symphonies, including the famous Fifth.",
      "[L3] Beethoven was known for going blind later in his life, yet continuing to compose."],
     "L3", "Beethoven went deaf, not blind, later in life.",
     ["deaf", "went deaf", "Beethoven went deaf, not blind"], "easy"),
]

for task_desc, lines, err_loc, correction, accepted, diff in factual_errors:
    prompt = make_header(task_desc) + "\n".join(lines)
    add_item(idx, prompt, err_loc, correction, accepted, diff, "factual")
    idx += 1

# ============================================================
# TYPE 2: Logical/reasoning errors (16 items) — Invalid inferences
# ============================================================
logical_errors = [
    ("Evaluate this logical argument.",
     ["[L1] All mammals are warm-blooded.",
      "[L2] All dogs are mammals.",
      "[L3] Therefore, all warm-blooded animals are dogs."],
     "L3", "The conclusion does not follow. The correct conclusion is 'all dogs are warm-blooded' (affirming the consequent fallacy).",
     ["all dogs are warm-blooded", "affirming the consequent", "invalid conclusion", "does not follow"], "easy"),

    ("Check this reasoning about correlation and causation.",
     ["[L1] Ice cream sales increase during summer months.",
      "[L2] Drowning incidents also increase during summer months.",
      "[L3] Therefore, eating ice cream causes drowning."],
     "L3", "Correlation does not imply causation. Both are independently correlated with warm weather/summer.",
     ["correlation does not imply causation", "confounding variable", "correlation not causation", "warm weather"], "easy"),

    ("Evaluate this statistical argument.",
     ["[L1] In a survey of 1,000 people, 60% said they exercise regularly.",
      "[L2] The survey was conducted at a gym.",
      "[L3] Therefore, 60% of the general population exercises regularly."],
     "L3", "The conclusion is invalid due to sampling bias — the survey at a gym is not representative of the general population.",
     ["sampling bias", "not representative", "selection bias", "biased sample"], "medium"),

    ("Check this conditional reasoning.",
     ["[L1] If it rains, the ground gets wet.",
      "[L2] The ground is wet.",
      "[L3] Therefore, it rained."],
     "L3", "This is the fallacy of affirming the consequent. The ground could be wet for other reasons (sprinklers, flooding).",
     ["affirming the consequent", "other reasons", "sprinklers", "does not necessarily follow"], "easy"),

    ("Evaluate this argument about averages.",
     ["[L1] The average salary in Department A is $80,000 (5 employees).",
      "[L2] The average salary in Department B is $60,000 (50 employees).",
      "[L3] Therefore, the average salary across both departments is $70,000."],
     "L3", "The combined average must be weighted by department size: (5×80000 + 50×60000)/55 ≈ $61,818, not the simple mean of the two averages.",
     ["weighted average", "$61,818", "61818", "must weight by department size"], "medium"),

    ("Check this argument about necessity and sufficiency.",
     ["[L1] Being over 18 is necessary to vote in most countries.",
      "[L2] John is over 18.",
      "[L3] Therefore, John can definitely vote."],
     "L3", "Being over 18 is necessary but not sufficient to vote. Other conditions apply (citizenship, registration, etc.).",
     ["not sufficient", "necessary but not sufficient", "citizenship", "other conditions"], "medium"),

    ("Evaluate this base rate reasoning.",
     ["[L1] A rare disease affects 1 in 10,000 people.",
      "[L2] A test for the disease has a 99% accuracy rate.",
      "[L3] If someone tests positive, there is a 99% chance they have the disease."],
     "L3", "Due to the base rate fallacy, the actual probability is much lower (~1%). Most positives from a rare disease are false positives.",
     ["base rate fallacy", "false positives", "much lower than 99%", "base rate"], "hard"),

    ("Check this argument about composition.",
     ["[L1] Every brick in this wall weighs 2 kilograms.",
      "[L2] Therefore, this wall is light.",
      "[L3] Light things are easy to move."],
     "L2", "This is the fallacy of composition. Individual bricks being light does not make the entire wall light.",
     ["fallacy of composition", "individual parts", "wall has many bricks"], "medium"),

    ("Evaluate this argument from authority.",
     ["[L1] Dr. Smith is a renowned physicist.",
      "[L2] Dr. Smith says that this new diet plan is the healthiest option.",
      "[L3] Therefore, this diet plan is the healthiest option."],
     "L3", "This is an appeal to authority fallacy. Dr. Smith's expertise is in physics, not nutrition or dietetics.",
     ["appeal to authority", "not an expert in nutrition", "irrelevant expertise", "wrong field"], "medium"),

    ("Check this probabilistic reasoning.",
     ["[L1] A fair coin has been flipped 9 times, landing heads each time.",
      "[L2] The coin is fair, so each flip is independent.",
      "[L3] Therefore, the next flip is more likely to be tails to 'balance out'."],
     "L3", "This is the gambler's fallacy. Each flip is independent; the probability of tails on the next flip remains 50%.",
     ["gambler's fallacy", "independent", "50%", "still 50%", "each flip is independent"], "easy"),

    ("Evaluate this categorical syllogism.",
     ["[L1] Some birds can fly.",
      "[L2] Penguins are birds.",
      "[L3] Therefore, penguins can fly."],
     "L3", "'Some birds can fly' does not imply all birds can fly. Penguins are flightless birds.",
     ["not all birds can fly", "penguins cannot fly", "flightless", "some does not mean all"], "easy"),

    ("Check this argument about percentages.",
     ["[L1] A store raises prices by 20%.",
      "[L2] Later, the store offers a 20% discount.",
      "[L3] The final price is the same as the original price."],
     "L3", "The final price is 96% of the original (1.20 × 0.80 = 0.96), not 100%. A 20% increase then 20% decrease does not cancel out.",
     ["96%", "0.96", "not the same", "does not cancel out", "1.20 × 0.80 = 0.96"], "medium"),

    ("Evaluate this ecological reasoning.",
     ["[L1] Wolves were reintroduced to Yellowstone National Park in 1995.",
      "[L2] After reintroduction, elk populations decreased.",
      "[L3] Therefore, wolves eating elk is the sole reason for the ecosystem recovery."],
     "L3", "Wolf reintroduction had cascading effects (trophic cascade) beyond just elk predation, including changes in elk behavior, vegetation recovery, and river patterns. 'Sole reason' is incorrect.",
     ["not the sole reason", "trophic cascade", "cascading effects", "multiple factors"], "hard"),

    ("Check this economic reasoning.",
     ["[L1] Country X doubled its money supply over 5 years.",
      "[L2] Country X's GDP also doubled over the same period.",
      "[L3] Therefore, the standard of living in Country X has doubled."],
     "L3", "Doubling the money supply alongside GDP does not mean the standard of living doubled. Inflation, income distribution, and real vs nominal GDP must be considered.",
     ["inflation", "real vs nominal", "standard of living not determined by GDP alone"], "hard"),

    ("Evaluate this survival analysis reasoning.",
     ["[L1] Hospital A has a higher mortality rate than Hospital B.",
      "[L2] Both hospitals serve similar populations.",
      "[L3] Therefore, Hospital A provides worse care than Hospital B."],
     "L2", "If Hospital A treats more severe cases (selection bias / Simpson's paradox), the comparison is invalid. The claim that they serve 'similar populations' is likely the hidden error.",
     ["Simpson's paradox", "severity of cases", "case mix", "selection bias"], "hard"),

    ("Check this reasoning about natural selection.",
     ["[L1] Giraffes with longer necks can reach more food in tall trees.",
      "[L2] Therefore, giraffes stretched their necks to reach higher branches.",
      "[L3] Over generations, this stretching was passed to offspring, resulting in long-necked giraffes."],
     "L2", "This describes Lamarckian inheritance (acquired traits), which is incorrect. Natural selection favors giraffes born with longer necks, not stretching.",
     ["Lamarckian", "natural selection", "born with longer necks", "acquired traits are not inherited"], "medium"),
]

for task_desc, lines, err_loc, correction, accepted, diff in logical_errors:
    prompt = make_header(task_desc) + "\n".join(lines)
    add_item(idx, prompt, err_loc, correction, accepted, diff, "logical")
    idx += 1

# ============================================================
# TYPE 3: Unit/dimensional errors (16 items)
# ============================================================
unit_errors = [
    ("Verify this unit conversion.",
     ["[L1] A marathon is 42.195 kilometers.",
      "[L2] To convert to miles, divide by 1.609: 42.195 / 1.609 ≈ 26.2 miles.",
      "[L3] To convert to meters, multiply by 10: 42.195 × 10 = 421.95 meters."],
     "L3", "To convert km to meters, multiply by 1000, not 10. 42.195 × 1000 = 42,195 meters.",
     ["multiply by 1000", "42195", "42,195 meters", "1000 not 10"], "easy"),

    ("Check this speed calculation.",
     ["[L1] A car travels 150 km in 2 hours.",
      "[L2] Average speed = distance / time = 150 / 2 = 75 km/h.",
      "[L3] Converting to m/s: 75 × 3.6 = 270 m/s."],
     "L3", "To convert km/h to m/s, divide by 3.6, not multiply. 75 / 3.6 ≈ 20.83 m/s.",
     ["divide by 3.6", "20.83", "20.8", "divide not multiply"], "medium"),

    ("Verify this area calculation.",
     ["[L1] A rectangular room is 5 meters by 4 meters.",
      "[L2] Area = 5 × 4 = 20 square meters.",
      "[L3] Converting to square feet: 20 × 3.281 = 65.62 square feet."],
     "L3", "To convert m² to ft², multiply by 3.281² ≈ 10.764, not 3.281. Answer: 20 × 10.764 ≈ 215.28 sq ft.",
     ["10.764", "215.28", "3.281 squared", "square the conversion factor"], "medium"),

    ("Check this temperature conversion.",
     ["[L1] Normal body temperature is 98.6°F.",
      "[L2] To convert to Celsius: (98.6 - 32) × 5/9 = 37°C.",
      "[L3] To convert to Kelvin: 37 + 373.15 = 410.15 K."],
     "L3", "To convert Celsius to Kelvin, add 273.15 (not 373.15). 37 + 273.15 = 310.15 K.",
     ["273.15", "310.15", "add 273.15 not 373.15"], "easy"),

    ("Verify this volume conversion.",
     ["[L1] A fish tank holds 50 gallons of water.",
      "[L2] Converting to liters: 50 × 3.785 = 189.25 liters.",
      "[L3] Converting to cubic meters: 189.25 / 100 = 1.8925 cubic meters."],
     "L3", "To convert liters to cubic meters, divide by 1000, not 100. 189.25 / 1000 = 0.18925 m³.",
     ["divide by 1000", "0.18925", "0.189", "1000 not 100"], "medium"),

    ("Check this energy conversion.",
     ["[L1] A light bulb uses 60 watts.",
      "[L2] Running for 10 hours uses 60 × 10 = 600 watt-hours.",
      "[L3] Converting to kilowatt-hours: 600 × 1000 = 600,000 kWh."],
     "L3", "To convert Wh to kWh, divide by 1000, not multiply. 600 / 1000 = 0.6 kWh.",
     ["divide by 1000", "0.6 kWh", "0.6", "divide not multiply"], "easy"),

    ("Verify this pressure calculation.",
     ["[L1] Standard atmospheric pressure is 101,325 pascals.",
      "[L2] This equals 101.325 kilopascals (divide by 1000).",
      "[L3] Converting to millibars: 101.325 × 100 = 10,132.5 millibars."],
     "L3", "1 kPa = 10 mbar, so 101.325 kPa = 1013.25 mbar (multiply by 10, not 100).",
     ["1013.25", "multiply by 10", "1013", "10 not 100"], "hard"),

    ("Check this distance-time calculation.",
     ["[L1] Light travels at approximately 3 × 10⁸ m/s.",
      "[L2] The Sun is about 1.5 × 10⁸ km from Earth.",
      "[L3] Light travel time = 1.5 × 10⁸ / 3 × 10⁸ = 0.5 seconds."],
     "L3", "Units mismatch: the distance is in km but speed is in m/s. Must convert km to m first: 1.5 × 10¹¹ m / 3 × 10⁸ m/s = 500 seconds ≈ 8.3 minutes.",
     ["500 seconds", "8.3 minutes", "unit mismatch", "convert km to m", "8 minutes"], "medium"),

    ("Verify this density calculation.",
     ["[L1] An object has mass 500 g and volume 200 cm³.",
      "[L2] Density = mass / volume = 500 / 200 = 2.5 g/cm³.",
      "[L3] Converting to kg/m³: 2.5 × 100 = 250 kg/m³."],
     "L3", "1 g/cm³ = 1000 kg/m³. So 2.5 g/cm³ = 2500 kg/m³ (multiply by 1000, not 100).",
     ["2500", "multiply by 1000", "2500 kg/m³", "1000 not 100"], "medium"),

    ("Check this data storage conversion.",
     ["[L1] A file is 2.5 gigabytes (GB) in size.",
      "[L2] Converting to megabytes: 2.5 × 1024 = 2560 MB.",
      "[L3] Converting to kilobytes: 2560 × 100 = 256,000 KB."],
     "L3", "To convert MB to KB, multiply by 1024, not 100. 2560 × 1024 = 2,621,440 KB.",
     ["multiply by 1024", "2621440", "2,621,440", "1024 not 100"], "medium"),

    ("Verify this force calculation.",
     ["[L1] A 10 kg mass experiences gravitational acceleration of 9.81 m/s².",
      "[L2] Force = mass × acceleration = 10 × 9.81 = 98.1 newtons.",
      "[L3] Converting to kilonewtons: 98.1 × 1000 = 98,100 kN."],
     "L3", "To convert N to kN, divide by 1000, not multiply. 98.1 / 1000 = 0.0981 kN.",
     ["divide by 1000", "0.0981", "divide not multiply"], "easy"),

    ("Check this time calculation.",
     ["[L1] A process takes 7,200 seconds.",
      "[L2] Converting to minutes: 7200 / 60 = 120 minutes.",
      "[L3] Converting to hours: 120 / 24 = 5 hours."],
     "L3", "To convert minutes to hours, divide by 60, not 24. 120 / 60 = 2 hours.",
     ["divide by 60", "2 hours", "60 not 24"], "easy"),

    ("Verify this fuel efficiency conversion.",
     ["[L1] A car achieves 35 miles per gallon (mpg).",
      "[L2] Converting to km/L: 35 × 1.609 / 3.785 = 14.87 km/L.",
      "[L3] Converting to L/100km: 14.87 × 100 = 1487 L/100km."],
     "L3", "L/100km = 100 / (km/L). So 100 / 14.87 ≈ 6.72 L/100km, not 14.87 × 100.",
     ["100 / km per liter", "6.72", "6.7", "reciprocal", "divide 100 by km/L"], "hard"),

    ("Check this electrical calculation.",
     ["[L1] A circuit has 12V and 2A of current.",
      "[L2] Power = V × I = 12 × 2 = 24 watts.",
      "[L3] Resistance = V / I² = 12 / 4 = 3 ohms."],
     "L3", "Ohm's law: R = V / I = 12 / 2 = 6 ohms. The formula V/I² is incorrect.",
     ["R = V / I", "6 ohms", "V/I not V/I²"], "medium"),

    ("Verify this biological measurement.",
     ["[L1] A healthy adult heart rate is approximately 72 beats per minute.",
      "[L2] In one hour, the heart beats 72 × 60 = 4,320 times.",
      "[L3] In one day, the heart beats 4,320 × 12 = 51,840 times."],
     "L3", "There are 24 hours in a day, not 12. 4,320 × 24 = 103,680 beats per day.",
     ["24 hours", "103,680", "103680", "24 not 12"], "easy"),

    ("Check this financial percentage calculation.",
     ["[L1] An investment grows from $1,000 to $1,500 over 3 years.",
      "[L2] Total return = ($1,500 - $1,000) / $1,000 = 50%.",
      "[L3] Annual return = 50% / 3 = 16.67% per year."],
     "L3", "Simple division gives simple average return, not compound annual return. CAGR = (1500/1000)^(1/3) - 1 ≈ 14.47%.",
     ["14.47%", "compound annual", "CAGR", "not simple division"], "hard"),
]

for task_desc, lines, err_loc, correction, accepted, diff in unit_errors:
    prompt = make_header(task_desc) + "\n".join(lines)
    add_item(idx, prompt, err_loc, correction, accepted, diff, "unit_dimensional")
    idx += 1

# ============================================================
# TYPE 4: Statistical/methodological errors (16 items)
# ============================================================
stat_errors = [
    ("Evaluate this research claim.",
     ["[L1] A study of 50 patients found that Drug A reduced symptoms in 70% of cases.",
      "[L2] The p-value was 0.03, which is below the 0.05 threshold.",
      "[L3] Therefore, Drug A is proven to cure the condition."],
     "L3", "'Statistically significant' does not mean 'proven to cure'. It means the result is unlikely due to chance alone. The study shows evidence of symptom reduction, not a cure.",
     ["not proven", "does not prove", "evidence not proof", "statistically significant is not proof"], "medium"),

    ("Check this interpretation of a confidence interval.",
     ["[L1] A poll estimates candidate support at 52% with a margin of error of ±3%.",
      "[L2] The 95% confidence interval is 49% to 55%.",
      "[L3] There is a 95% probability that the true support is between 49% and 55%."],
     "L3", "Frequentist confidence intervals don't assign probability to the parameter. The correct interpretation is: if we repeated this poll many times, 95% of the intervals would contain the true value.",
     ["doesn't assign probability", "repeated sampling", "frequentist interpretation", "not a probability statement about the parameter"], "hard"),

    ("Verify this sample size reasoning.",
     ["[L1] We surveyed 30 people from a city of 1,000,000.",
      "[L2] 80% of respondents preferred Brand A.",
      "[L3] We can confidently say 80% of the entire city prefers Brand A."],
     "L3", "A sample of 30 is too small for reliable generalization to 1,000,000 people. The margin of error would be very large (~14-18%).",
     ["too small", "sample size", "margin of error", "cannot generalize from 30"], "easy"),

    ("Check this regression interpretation.",
     ["[L1] A regression model shows R² = 0.85 for predicting house prices.",
      "[L2] This means the model explains 85% of the variance in house prices.",
      "[L3] Therefore, the model's predictions are 85% accurate."],
     "L3", "R² measures variance explained, not prediction accuracy. An R² of 0.85 does not mean 85% of predictions are correct.",
     ["not prediction accuracy", "variance explained", "R² is not accuracy"], "medium"),

    ("Evaluate this claim about outliers.",
     ["[L1] The average household income in our sample is $250,000.",
      "[L2] The median household income is $48,000.",
      "[L3] The data shows that most households earn around $250,000."],
     "L3", "The large gap between mean ($250K) and median ($48K) indicates the mean is skewed by outliers. Most households earn closer to $48,000.",
     ["skewed by outliers", "median is more representative", "$48,000", "outliers inflate the mean"], "medium"),

    ("Check this A/B test conclusion.",
     ["[L1] Version A had a 2.1% conversion rate and Version B had a 2.3% conversion rate.",
      "[L2] The test ran for 2 days with 50 visitors per version.",
      "[L3] Version B is statistically significantly better than Version A."],
     "L3", "With only 50 visitors per version and a 0.2% difference, the sample size is far too small for statistical significance.",
     ["sample too small", "not statistically significant", "insufficient sample", "50 is too few"], "medium"),

    ("Verify this survivorship bias example.",
     ["[L1] We studied 100 successful startups to find common traits.",
      "[L2] 90% had founders with technical backgrounds.",
      "[L3] Therefore, having a technical founder significantly increases startup success."],
     "L3", "This conclusion suffers from survivorship bias. Without studying failed startups (with or without technical founders), you can't draw this causal conclusion.",
     ["survivorship bias", "failed startups", "need to study failures", "selection on the outcome"], "medium"),

    ("Check this misinterpretation of averages.",
     ["[L1] The average number of legs per person in this room is 1.98.",
      "[L2] This means some people in the room have fewer than 2 legs.",
      "[L3] This is unusual and suggests a high proportion of amputees."],
     "L3", "An average of 1.98 legs only requires a very small fraction of people with fewer than 2 legs. With 100 people, just 1 amputee gives an average of 1.99. This is not unusual.",
     ["not unusual", "very few amputees needed", "small fraction", "one or two people"], "medium"),

    ("Evaluate this ecological fallacy.",
     ["[L1] Countries with higher average chocolate consumption have more Nobel laureates per capita.",
      "[L2] There is a strong positive correlation (r = 0.79).",
      "[L3] Therefore, eating chocolate improves individual cognitive ability."],
     "L3", "This is the ecological fallacy — correlations at the country level cannot be applied to individuals. The correlation likely reflects confounding factors (wealth, education, research funding).",
     ["ecological fallacy", "country-level", "confounding factors", "cannot apply to individuals"], "hard"),

    ("Check this misuse of standard deviation.",
     ["[L1] Test scores have a mean of 75 and a standard deviation of 10.",
      "[L2] The range of one standard deviation from the mean is 65 to 85.",
      "[L3] Therefore, exactly 68% of students scored between 65 and 85."],
     "L3", "The 68% rule (empirical rule) only applies to normally distributed data. Without knowing the distribution, we cannot claim exactly 68%.",
     ["normal distribution", "only if normally distributed", "empirical rule assumes normality", "distribution not specified"], "hard"),

    ("Verify this claim about multiple comparisons.",
     ["[L1] We tested 20 different foods for correlation with cancer.",
      "[L2] One food showed a p-value of 0.04.",
      "[L3] This food is significantly correlated with cancer risk."],
     "L3", "With 20 tests at α=0.05, we expect ~1 false positive by chance. This is the multiple comparisons problem; correction (e.g., Bonferroni) is needed.",
     ["multiple comparisons", "Bonferroni", "false positive", "expected by chance", "multiple testing"], "hard"),

    ("Check this interpretation of relative risk.",
     ["[L1] Drug X doubles the risk of a rare side effect.",
      "[L2] The baseline risk is 1 in 100,000.",
      "[L3] Therefore, Drug X is extremely dangerous and should be banned."],
     "L3", "Doubling a 1/100,000 risk means it becomes 2/100,000 — still extremely rare. The absolute risk increase is tiny (0.001%). Relative risk alone is misleading.",
     ["absolute risk", "still very rare", "0.001%", "relative vs absolute risk"], "medium"),

    ("Evaluate this selection bias in surveys.",
     ["[L1] An online poll received 50,000 responses about public transit satisfaction.",
      "[L2] 85% of respondents expressed dissatisfaction.",
      "[L3] Therefore, 85% of the population is dissatisfied with public transit."],
     "L3", "Online polls suffer from self-selection bias — people with strong negative opinions are more likely to respond. This is not representative of the general population.",
     ["self-selection bias", "not representative", "voluntary response bias"], "easy"),

    ("Verify this claim about extrapolation.",
     ["[L1] A child grew 3 inches per year between ages 5 and 10.",
      "[L2] This linear growth rate was consistent over the 5-year period.",
      "[L3] At this rate, by age 40 the child will be 7 feet 6 inches tall."],
     "L3", "Linear extrapolation of childhood growth rates is invalid because growth slows and stops during adolescence.",
     ["growth stops", "puberty", "cannot extrapolate", "growth is not linear indefinitely"], "easy"),

    ("Check this correlation coefficient interpretation.",
     ["[L1] The correlation between study hours and exam scores is r = 0.45.",
      "[L2] This indicates a moderate positive relationship.",
      "[L3] Study hours explain 45% of the variance in exam scores."],
     "L3", "R² = 0.45² = 0.2025. Study hours explain approximately 20% of the variance, not 45%.",
     ["20%", "R² = 0.2025", "r squared", "0.45 squared", "20.25%"], "medium"),

    ("Evaluate this reasoning about sample representativeness.",
     ["[L1] A newspaper poll surveyed 10,000 of its subscribers about media trust.",
      "[L2] The large sample size (n=10,000) ensures high statistical power.",
      "[L3] The results are therefore representative of the general public's views on media trust."],
     "L3", "Newspaper subscribers are not representative of the general public. Large sample size does not compensate for a biased sampling frame.",
     ["not representative", "biased sample", "subscribers are not general public", "sample size doesn't fix bias"], "medium"),
]

for task_desc, lines, err_loc, correction, accepted, diff in stat_errors:
    prompt = make_header(task_desc) + "\n".join(lines)
    add_item(idx, prompt, err_loc, correction, accepted, diff, "statistical")
    idx += 1

# ============================================================
# TYPE 5: Definitional/category errors (16 items)
# ============================================================
def_errors = [
    ("Verify this biological classification.",
     ["[L1] A whale is a large fish that lives in the ocean.",
      "[L2] Whales breathe air using lungs and nurse their young.",
      "[L3] Blue whales are the largest animals ever to have lived on Earth."],
     "L1", "Whales are mammals, not fish.",
     ["mammals", "whales are mammals", "marine mammals"], "easy"),

    ("Check this description of states of matter.",
     ["[L1] Water freezes at 0°C and boils at 100°C at standard atmospheric pressure.",
      "[L2] Glass is a liquid that flows very slowly at room temperature.",
      "[L3] Metals expand when heated due to increased atomic vibration."],
     "L2", "Glass is an amorphous solid, not a liquid. The idea that glass flows slowly is a popular myth.",
     ["amorphous solid", "glass is a solid", "not a liquid", "myth"], "medium"),

    ("Verify this classification of fruits and vegetables.",
     ["[L1] Tomatoes are vegetables commonly used in salads and sauces.",
      "[L2] Botanically, fruits develop from the flower of a plant and contain seeds.",
      "[L3] Lettuce and carrots are examples of vegetable plant parts."],
     "L1", "Botanically, tomatoes are fruits (they develop from the flower and contain seeds), not vegetables.",
     ["fruit", "tomatoes are fruits", "botanically a fruit"], "easy"),

    ("Check this description of computing concepts.",
     ["[L1] RAM (Random Access Memory) is a type of permanent storage.",
      "[L2] Hard drives store data magnetically on spinning platters.",
      "[L3] SSDs use flash memory chips with no moving parts."],
     "L1", "RAM is volatile (temporary) memory, not permanent storage. Data in RAM is lost when power is turned off.",
     ["volatile", "temporary", "not permanent", "lost when powered off"], "easy"),

    ("Verify this description of the immune system.",
     ["[L1] Antibiotics are effective against both bacterial and viral infections.",
      "[L2] Vaccines stimulate the immune system to produce antibodies.",
      "[L3] White blood cells are a key component of the immune response."],
     "L1", "Antibiotics are effective only against bacterial infections, not viral infections.",
     ["only bacterial", "not effective against viruses", "antibiotics don't work on viruses"], "easy"),

    ("Check this description of economic systems.",
     ["[L1] In a free market economy, prices are determined by supply and demand.",
      "[L2] Inflation occurs when the general price level rises over time.",
      "[L3] A recession is defined as two consecutive quarters of rising GDP."],
     "L3", "A recession is commonly defined as two consecutive quarters of declining (not rising) GDP.",
     ["declining GDP", "falling GDP", "negative GDP growth", "shrinking economy"], "easy"),

    ("Verify this description of musical concepts.",
     ["[L1] An octave spans 12 semitones in Western music.",
      "[L2] A major scale consists of 7 notes with a specific pattern of whole and half steps.",
      "[L3] The tempo of a piece is measured in decibels."],
     "L3", "Tempo is measured in beats per minute (BPM), not decibels. Decibels measure sound intensity/loudness.",
     ["beats per minute", "BPM", "decibels measure loudness", "not decibels"], "easy"),

    ("Check this description of legal concepts.",
     ["[L1] In criminal law, the prosecution must prove guilt beyond a reasonable doubt.",
      "[L2] In civil law, the standard is the preponderance of evidence (more likely than not).",
      "[L3] The defendant in a criminal trial must prove their innocence."],
     "L3", "In criminal law, the defendant is presumed innocent. The burden of proof lies with the prosecution, not the defendant.",
     ["presumed innocent", "burden on prosecution", "prosecution must prove guilt"], "medium"),

    ("Verify this astronomical description.",
     ["[L1] A light-year is a unit of distance, equal to the distance light travels in one year.",
      "[L2] The nearest star to Earth (besides the Sun) is Proxima Centauri, about 4.24 light-years away.",
      "[L3] A black hole is a region where gravity is so strong that even light cannot escape its event horizon.",
      "[L4] Shooting stars are stars that fall from their position in the galaxy."],
     "L4", "Shooting stars are not stars. They are meteors — small particles burning up in Earth's atmosphere.",
     ["meteors", "not actual stars", "particles in atmosphere", "meteoroids"], "easy"),

    ("Check this description of plant biology.",
     ["[L1] Plants produce oxygen during photosynthesis.",
      "[L2] Roots absorb water and minerals from the soil.",
      "[L3] Trees grow their trunks only from the bottom, pushing the whole tree upward."],
     "L3", "Trees grow from the tips (apical meristems) and increase in girth via cambium. They do not grow by pushing upward from the bottom.",
     ["apical meristems", "grow from tips", "not from the bottom", "cambium"], "medium"),

    ("Verify this description of weather phenomena.",
     ["[L1] Thunder is caused by the rapid expansion of air heated by lightning.",
      "[L2] Tornadoes are classified using the Enhanced Fujita (EF) scale.",
      "[L3] Hurricanes form over cold northern ocean waters."],
     "L3", "Hurricanes form over warm tropical ocean waters (typically above 26.5°C), not cold northern waters.",
     ["warm tropical", "warm water", "26.5°C", "tropical oceans"], "easy"),

    ("Check this description of the scientific method.",
     ["[L1] A hypothesis is a testable prediction about the outcome of an experiment.",
      "[L2] A theory in science is merely a guess that has not been tested.",
      "[L3] Peer review is the process of having other scientists evaluate research before publication."],
     "L2", "In science, a theory is a well-substantiated explanation supported by extensive evidence, not merely a guess.",
     ["well-substantiated", "supported by evidence", "not a guess", "extensively tested"], "medium"),

    ("Verify this description of nutrition.",
     ["[L1] Carbohydrates, proteins, and fats are the three macronutrients.",
      "[L2] Vitamins and minerals are micronutrients needed in smaller amounts.",
      "[L3] All fats are unhealthy and should be eliminated from the diet."],
     "L3", "Not all fats are unhealthy. Unsaturated fats (found in olive oil, nuts, fish) are essential for health.",
     ["not all fats are unhealthy", "unsaturated fats", "healthy fats", "essential fatty acids"], "easy"),

    ("Check this description of geological time.",
     ["[L1] The age of the Earth is approximately 4.54 billion years.",
      "[L2] Dinosaurs went extinct about 66 million years ago.",
      "[L3] Humans and dinosaurs coexisted for millions of years before the extinction event."],
     "L3", "Humans and dinosaurs did not coexist. Modern humans appeared roughly 300,000 years ago, about 65 million years after non-avian dinosaurs went extinct.",
     ["did not coexist", "65 million years apart", "humans appeared much later"], "easy"),

    ("Verify this description of semiconductor physics.",
     ["[L1] Semiconductors have electrical conductivity between that of conductors and insulators.",
      "[L2] Silicon is the most widely used semiconductor material.",
      "[L3] Superconductors are semiconductors that work at very high temperatures."],
     "L3", "Superconductors are distinct from semiconductors. Superconductors exhibit zero electrical resistance, typically at very low temperatures (not high).",
     ["zero resistance", "low temperatures", "not semiconductors", "superconductors are different"], "medium"),

    ("Check this description of language families.",
     ["[L1] English belongs to the Germanic branch of the Indo-European language family.",
      "[L2] Mandarin Chinese is a tonal language in the Sino-Tibetan family.",
      "[L3] Arabic and Hebrew are Romance languages derived from Latin."],
     "L3", "Arabic and Hebrew are Semitic languages (Afro-Asiatic family), not Romance languages. Romance languages (French, Spanish, Italian) are derived from Latin.",
     ["Semitic", "Afro-Asiatic", "not Romance", "not derived from Latin"], "medium"),
]

for task_desc, lines, err_loc, correction, accepted, diff in def_errors:
    prompt = make_header(task_desc) + "\n".join(lines)
    add_item(idx, prompt, err_loc, correction, accepted, diff, "definitional")
    idx += 1


# ============================================================
# Final output
# ============================================================
print(f"Generated {len(items)} CR items (target: 80)")

# Verify error position variety
locs = [i["error_location"] for i in items]
print(f"  Error positions: L1={locs.count('L1')} L2={locs.count('L2')} L3={locs.count('L3')} L4={locs.count('L4')}")

# Verify error type variety
types = {}
for i in items:
    t = i.get("error_type", "unknown")
    types[t] = types.get(t, 0) + 1
print(f"  Error types: {types}")

# Verify difficulty distribution
diffs = [i["difficulty"] for i in items]
print(f"  Difficulty: easy={diffs.count('easy')} medium={diffs.count('medium')} hard={diffs.count('hard')}")

with open("_cr_items.json", "w", encoding="utf-8") as f:
    json.dump(items, f, indent=2, ensure_ascii=False)
print(f"Wrote {len(items)} CR items to _cr_items.json")
