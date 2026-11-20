
import json
from pathlib import Path

path = Path("data/processed/kau_english_pages.json")

with open(path, encoding="utf-8") as f:
    pages = json.load(f)

page_map = {p["page"]: p["text"] for p in pages}

page_220 = page_map[220]
page_221 = page_map[221]

start_heading = "Bunchy top disease"
next_heading = "Panama wilt"

start = page_220.find(start_heading)
end = page_221.find(next_heading)

if start == -1 or end == -1:
    raise ValueError("Expected section headings not found.")

part_1 = page_220[start:]
part_2 = page_221[:end]

# Remove verified page footer from page 220
part_1 = part_1.replace("BANANA\n212", "").strip()

combined = part_1 + "\n" + part_2.strip()

record = {
    "chunk_id": "banana_bunchy_top_test",
    "crop": "banana",
    "section_heading": "Bunchy top disease",
    "pdf_pages": [220, 221],
    "text": combined
}

output = Path("data/processed/banana_cross_page_test.json")

with open(output, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print("SECTION:", record["section_heading"])
print("PDF PAGES:", record["pdf_pages"])
print("CHARACTERS:", len(combined))
print("\nFULL SECTION:")
print("=" * 60)
print(combined)
print("\nSaved to:", output)
