
import json
from pathlib import Path

INPUT = Path("data/processed/banana_clean_pages.json")
OUTPUT = Path("data/processed/banana_page_map.json")

with open(INPUT, encoding="utf-8") as f:
    pages = json.load(f)

full_text = ""
page_spans = []

for page in pages:
    if full_text:
        full_text += "\n"

    start = len(full_text)
    full_text += page["text"]
    end = len(full_text)

    page_spans.append({
        "pdf_page": page["pdf_page"],
        "start": start,
        "end": end
    })

result = {
    "crop": "banana",
    "text": full_text,
    "page_spans": page_spans
}

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Pages mapped:", len(page_spans))
print("Total characters:", len(full_text))

print("\nPage spans:")
for span in page_spans:
    print(
        f"PDF page {span['pdf_page']}: "
        f"{span['start']} to {span['end']}"
    )

# Verify that each mapped span matches the original cleaned page
all_valid = all(
    full_text[span["start"]:span["end"]] == page["text"]
    for span, page in zip(page_spans, pages)
)

print("\nAll page mappings valid:", all_valid)
print("Saved to:", OUTPUT)
