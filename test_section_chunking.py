
import json
from pathlib import Path

input_path = Path("data/processed/kau_english_pages.json")
output_path = Path("data/processed/banana_sections_test.json")

with open(input_path, encoding="utf-8") as f:
    pages = json.load(f)

page = next(
    p for p in pages
    if p["page"] == 222
)

text = page["text"]

# Known headings verified from the original PDF page
headings = [
    "Infectious chlorosis (Cucumber mosaic",
    "Banana streak disease",
    "Process Protocol for Banana flour",
    "RTE Snacks from starch based food"
]

positions = []

for heading in headings:
    position = text.find(heading)

    if position == -1:
        raise ValueError(
            f"Heading not found: {heading}"
        )

    positions.append((position, heading))

positions.sort()

sections = []

for i, (start, heading) in enumerate(positions):
    end = (
        positions[i + 1][0]
        if i + 1 < len(positions)
        else len(text)
    )

    section_text = text[start:end].strip()

    sections.append({
        "chunk_id": f"banana_222_section_{i + 1}",
        "crop": "banana",
        "source": page["source"],
        "publication_year": page["publication_year"],
        "pdf_page": 222,
        "section_heading": heading,
        "text": section_text
    })

output_path.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(
        sections,
        f,
        ensure_ascii=False,
        indent=2
    )

print("Sections extracted:", len(sections))

for section in sections:
    print("\n" + "=" * 60)
    print("ID:", section["chunk_id"])
    print("Heading:", section["section_heading"])
    print("Characters:", len(section["text"]))
    print("Beginning:", section["text"][:160])
    print("Ending:", section["text"][-160:])

print("\nSaved to:", output_path)
