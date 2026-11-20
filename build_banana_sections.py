
import json
from pathlib import Path

INPUT = Path("data/processed/banana_page_map.json")
OUTPUT = Path("data/processed/banana_structured_sections.json")

with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)

text = data["text"]
page_spans = data["page_spans"]

# Boundaries verified against the KAU banana chapter
section_boundaries = [
    ("Bunchy top disease", "Panama wilt"),
    ("Infectious chlorosis (Cucumber mosaic",
     "Banana streak disease"),
    ("Banana streak disease",
     "Process Protocol for Banana flour"),
    ("Process Protocol for Banana flour",
     "RTE Snacks from starch based food")
]


def extract_section(start_heading, end_heading, index):
    start = text.find(start_heading)

    if start == -1:
        raise ValueError(
            f"Heading not found: {start_heading}"
        )

    end = text.find(end_heading, start + len(start_heading))

    if end == -1:
        raise ValueError(
            f"End heading not found: {end_heading}"
        )

    source_pages = [
        span["pdf_page"]
        for span in page_spans
        if span["start"] < end and span["end"] > start
    ]

    return {
        "chunk_id": f"banana_section_{index:03d}",
        "crop": "banana",
        "source": "KAU Package of Practices 2016",
        "section_heading": start_heading,
        "pdf_pages": source_pages,
        "start_offset": start,
        "end_offset": end,
        "text": text[start:end].strip()
    }


sections = []

for index, (start_heading, end_heading) in enumerate(
    section_boundaries, start=1
):
    sections.append(
        extract_section(start_heading, end_heading, index)
    )

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(sections, f, ensure_ascii=False, indent=2)

print("Sections created:", len(sections))

for section in sections:
    print("\n" + "=" * 55)
    print("ID:", section["chunk_id"])
    print("Heading:", section["section_heading"])
    print("Pages:", section["pdf_pages"])
    print("Characters:", len(section["text"]))

print("\nSaved to:", OUTPUT)
