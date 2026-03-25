"""Combine partial JSON files into metacog_dataset.json"""
import json

kbd = json.load(open("_kbd_items.json", encoding="utf-8"))
ccc = json.load(open("_ccc_items.json", encoding="utf-8"))
cr  = json.load(open("_cr_items.json", encoding="utf-8"))

dataset = kbd + ccc + cr
print(f"Combined: {len(kbd)} KBD + {len(ccc)} CCC + {len(cr)} CR = {len(dataset)} total")

# Validate JSON serialization
json_str = json.dumps(dataset, indent=2, ensure_ascii=False)
json.loads(json_str)  # verify round-trip
print("JSON round-trip OK")

with open("metacog_dataset.json", "w", encoding="utf-8") as f:
    f.write(json_str)
print("Wrote metacog_dataset.json")
