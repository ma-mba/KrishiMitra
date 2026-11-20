
import json
import re
from pathlib import Path

INPUT = Path("data/processed/kau_english_pages.json")
OUTPUT = Path("data/processed/banana_clean_pages.json")

with open(INPUT, encoding="utf-8") as f:
    pages = json.load(f)

cleaned_pages = []

for page in pages:
    page_num = page["page"]

    if not 216 <= page_num <= 222:
        continue

    lines = page["text"].splitlines()
    cleaned_lines = []

    for line in lines:
        stripped = line.strip()

        # Remove verified running headers/footers only
        if stripped in {"BANANA", "FRUITS"}:
            continue

        # Printed page numbers for PDF pages 216-222
        printed_page = str(page_num - 8)

        if stripped == printed_page:
            continue

        cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines).strip()

    cleaned_pages.append({
        "pdf_page": page_num,
        "text": cleaned_text
    })

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(
        cleaned_pages,
        f,
        ensure_ascii=False,
        indent=2
    )

print("Pages processed:", len(cleaned_pages))

for page in cleaned_pages:
    print(
        f"PDF page {page['pdf_page']}: "
        f"{len(page['text'])} characters"
    )

print("\nSaved to:", OUTPUT)
