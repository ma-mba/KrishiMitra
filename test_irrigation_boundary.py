
import json
from pathlib import Path

with open(
    "data/processed/kau_english_pages.json",
    encoding="utf-8"
) as f:
    pages = json.load(f)

page_map = {p["page"]: p["text"] for p in pages}

page_217 = page_map[217]
page_218 = page_map[218]

start_text = "For Palayankodan (rainfed), planting may"
end_text = "After planting banana, sow sun hemp"

start = page_217.find(start_text)
end = page_218.find(end_text)

if start == -1 or end == -1:
    raise ValueError("Expected text boundary not found.")

part_1 = page_217[start:]
part_2 = page_218[:end]

# Remove verified PDF footer
part_1 = part_1.replace("209\nBANANA", "").strip()

combined = part_1 + " " + part_2.strip()

print("PDF pages: 217-218")
print("Characters:", len(combined))
print("\nRECONSTRUCTED RECOMMENDATION:")
print("=" * 60)
print(combined)
