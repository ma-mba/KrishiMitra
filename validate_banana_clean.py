
import json
from pathlib import Path

path = Path("data/processed/banana_clean_pages.json")

with open(path, encoding="utf-8") as f:
    pages = json.load(f)

expected_pages = list(range(216, 223))
actual_pages = [p["pdf_page"] for p in pages]

print("1. Correct pages:", actual_pages == expected_pages)

for page in pages:
    number = page["pdf_page"]
    lines = [line.strip() for line in page["text"].splitlines()]

    unwanted = {"BANANA", "FRUITS", str(number - 8)}
    remaining = unwanted.intersection(lines)

    print(
        f"Page {number}: "
        f"remaining headers/footers = {sorted(remaining)}"
    )

full_text = "\n".join(p["text"] for p in pages)

required_phrases = [
    "Bunchy top disease",
    "Banana streak disease",
    "Infectious chlorosis",
    "For Palayankodan (rainfed), planting may",
    "Process Protocol for Banana flour"
]

print("\n2. Important content preserved:")

for phrase in required_phrases:
    print(f"{phrase}: {phrase in full_text}")

print("\n3. Empty pages:", [
    p["pdf_page"] for p in pages
    if not p["text"].strip()
])
