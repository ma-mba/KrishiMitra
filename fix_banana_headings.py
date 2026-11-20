
import json
from pathlib import Path

INPUT = Path("data/processed/banana_structured_sections.json")
OUTPUT = Path("data/processed/banana_sections_corrected.json")

with open(INPUT, encoding="utf-8") as f:
    sections = json.load(f)

heading_corrections = {
    "Infectious chlorosis (Cucumber mosaic":
        "Infectious chlorosis (Cucumber mosaic virus disease)",
    "Process Protocol for Banana flour":
        "Process Protocol for Banana flour production"
}

for section in sections:
    old_heading = section["section_heading"]

    section["section_heading"] = heading_corrections.get(
        old_heading,
        old_heading
    )

    # Preserve the original source text
    section["original_text"] = section["text"]

    # Store the original heading for auditability
    section["original_heading"] = old_heading

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(sections, f, ensure_ascii=False, indent=2)

print("Corrected sections:", len(sections))

for section in sections:
    print("\nID:", section["chunk_id"])
    print("Heading:", section["section_heading"])
    print("Pages:", section["pdf_pages"])

print("\nSaved to:", OUTPUT)
