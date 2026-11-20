
from pathlib import Path
import pymupdf
import json

raw_folder = Path("data/raw")
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

matches = list(raw_folder.rglob("pop2016.pdf"))

if not matches:
    raise FileNotFoundError("English KAU crop guide not found")

pdf_path = matches[0]
records = []

with pymupdf.open(pdf_path) as doc:
    for page_number, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()

        if not text:
            continue

        records.append({
            "document": pdf_path.name,
            "source": "Kerala Agricultural University",
            "language": "en",
            "publication_year": 2016,
            "page": page_number,
            "text": text
        })

output_path = output_folder / "kau_english_pages.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print("Source:", pdf_path.name)
print("Pages extracted:", len(records))
print("Saved to:", output_path)

if records:
    print("\nExample record:")
    print("Page:", records[0]["page"])
    print("Text:", records[0]["text"][:300])

