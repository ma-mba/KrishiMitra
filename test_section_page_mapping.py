
import json
from pathlib import Path

INPUT = Path("data/processed/banana_page_map.json")

with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)

text = data["text"]
page_spans = data["page_spans"]


def find_section(start_heading, end_heading):
    start = text.find(start_heading)

    if start == -1:
        raise ValueError(
            f"Start heading not found: {start_heading}"
        )

    end = text.find(end_heading, start + len(start_heading))

    if end == -1:
        raise ValueError(
            f"End heading not found: {end_heading}"
        )

    section_text = text[start:end].strip()

    source_pages = [
        span["pdf_page"]
        for span in page_spans
        if span["start"] < end and span["end"] > start
    ]

    return {
        "heading": start_heading,
        "pdf_pages": source_pages,
        "characters": len(section_text),
        "text": section_text
    }


tests = [
    (
        "Bunchy top disease",
        "Panama wilt"
    ),
    (
        "Banana streak disease",
        "Process Protocol for Banana flour"
    )
]

for start_heading, end_heading in tests:
    result = find_section(start_heading, end_heading)

    print("\n" + "=" * 60)
    print("SECTION:", result["heading"])
    print("PDF PAGES:", result["pdf_pages"])
    print("CHARACTERS:", result["characters"])
    print("BEGINNING:", result["text"][:120])
    print("ENDING:", result["text"][-120:])
