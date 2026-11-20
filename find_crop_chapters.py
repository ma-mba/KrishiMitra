
import json
import re
from pathlib import Path

path = Path("data/processed/kau_english_pages.json")

with open(path, "r", encoding="utf-8") as f:
    pages = json.load(f)

crops = {
    "RICE": re.compile(r"^\s*RICE\s*$", re.I),
    "BANANA": re.compile(r"^\s*BANANA\s*$", re.I),
    "COCONUT": re.compile(r"^\s*COCONUT\s*$", re.I),
}

for crop, pattern in crops.items():
    print("\n" + "=" * 55)
    print("CROP:", crop)

    matches = []

    for page in pages:
        lines = page["text"].splitlines()

        for index, line in enumerate(lines):
            if pattern.fullmatch(line.strip()):
                matches.append({
                    "page": page["page"],
                    "context": "\n".join(
                        lines[max(0, index-2):index+5]
                    )
                })

    print("Pages with exact heading:", len(matches))
    print("PDF page numbers:", [m["page"] for m in matches])

    print("\nFirst 5 examples:")
    for match in matches[:5]:
        print(f"\nPDF PAGE {match['page']}")
        print(match["context"])
        print("-" * 35)
