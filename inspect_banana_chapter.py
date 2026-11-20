
import json
from pathlib import Path

input_path = Path("data/processed/kau_english_pages.json")
output_path = Path("data/processed/banana_chapter_inspection.txt")

with open(input_path, "r", encoding="utf-8") as f:
    pages = json.load(f)

banana_pages = [
    page for page in pages
    if 216 <= page["page"] <= 222
]

with open(output_path, "w", encoding="utf-8") as f:
    for page in banana_pages:
        lines = [
            line.strip()
            for line in page["text"].splitlines()
            if line.strip()
        ]

        header = f"\n{'=' * 60}\nPDF PAGE {page['page']}\n{'=' * 60}\n"

        print(header)
        f.write(header)

        print("FIRST 12 LINES:")
        f.write("FIRST 12 LINES:\n")

        for line in lines[:12]:
            print(line)
            f.write(line + "\n")

        print("\nLAST 12 LINES:")
        f.write("\nLAST 12 LINES:\n")

        for line in lines[-12:]:
            print(line)
            f.write(line + "\n")

print("\nSaved to:", output_path)
