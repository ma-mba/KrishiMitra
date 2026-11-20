
import json
from pathlib import Path

path = Path("data/processed/kau_english_pages.json")

with open(path, "r", encoding="utf-8") as f:
    pages = json.load(f)

page_lookup = {page["page"]: page["text"] for page in pages}

# Candidate transitions, not yet confirmed boundaries
ranges = {
    "RICE": range(8, 54),
    "COCONUT": range(102, 124),
    "BANANA": range(213, 228)
}

for crop, page_range in ranges.items():
    print("\n" + "=" * 65)
    print("CHECKING:", crop)

    for page_number in page_range:
        text = page_lookup.get(page_number, "")

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        preview = " | ".join(lines[:5])

        print(
            f"PDF PAGE {page_number:3}: "
            f"{preview[:125]}"
        )
