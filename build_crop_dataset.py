
import json
from pathlib import Path

input_path = Path("data/processed/kau_english_chunks.json")
output_path = Path("data/processed/kau_crop_chunks.json")

crop_ranges = {
    "rice": (9, 49),
    "coconut": (104, 119),
    "banana": (216, 222)
}

with open(input_path, "r", encoding="utf-8") as f:
    chunks = json.load(f)

crop_chunks = []

for chunk in chunks:
    page = chunk["page"]

    for crop, (start, end) in crop_ranges.items():
        if start <= page <= end:
            record = chunk.copy()
            record["crop"] = crop
            record["pdf_page"] = page
            record["chunk_id"] = f"{crop}_{chunk['chunk_id']}"
            crop_chunks.append(record)
            break

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(
        crop_chunks,
        f,
        ensure_ascii=False,
        indent=2
    )

print("Original chunks:", len(chunks))
print("Crop-specific chunks:", len(crop_chunks))
print("Saved to:", output_path)

for crop in crop_ranges:
    selected = [
        c for c in crop_chunks
        if c["crop"] == crop
    ]
    print(f"{crop.title()}: {len(selected)} chunks")

print("\nExample record:")
if crop_chunks:
    example = crop_chunks[0]
    print("ID:", example["chunk_id"])
    print("Crop:", example["crop"])
    print("PDF page:", example["pdf_page"])
    print("Text:", example["text"][:250])
